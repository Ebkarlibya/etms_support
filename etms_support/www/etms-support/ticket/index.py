import frappe
from urllib.parse import urljoin

def get_context(ctx):
    ctx.no_cache = 1
    user = frappe.session.user
    query = frappe.request.query_string
    target_ticket = query.decode('utf-8').split("=")[1]
    
    ticket = frappe.get_doc("Tickets", target_ticket)
    attachment_path = frappe.get_all("File", fields="file_url", filters={
        "attached_to_doctype": "Tickets",
        "attached_to_name": ticket.name
    })
    if len(attachment_path) > 0:
        ctx['attachment_url'] = urljoin(ctx.url, attachment_path[0].file_url)

    ctx['target_ticket'] = target_ticket
    ctx['ticket'] = ticket