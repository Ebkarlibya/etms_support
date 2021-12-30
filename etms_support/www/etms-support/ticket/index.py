import frappe
import json
from urllib.parse import urljoin

def get_context(ctx):
    ctx.no_cache = 1
    user = frappe.session.user
    query = frappe.request.query_string
    target_ticket = query.decode('utf-8').split("=")[1]
    
    ticket = frappe.get_doc("Issue", target_ticket)
    user_details = frappe.get_all("User", fields=["full_name", "user_image"], filters={
        "name": ticket.raised_by
    })[0]
    attachment_path = frappe.get_all("File", fields="file_url", filters={
        "attached_to_doctype": "Tickets",
        "attached_to_name": ticket.name
    })
    if len(attachment_path) > 0:
        ctx['attachment_url'] = urljoin(ctx.url, attachment_path[0].file_url)

    # append user name and image to each comment user
    comments = frappe.get_all("Comment", fields=["creation", "comment_email", "content"], filters={
        "reference_doctype": "Issue",
        "reference_name": ticket.name
    })
    for comment in comments:
        comment['user_details'] = frappe.get_all("User", 
            fields=["full_name", "user_image"],
            filters={"name": comment.comment_email})[0]


    ctx['user_details'] = user_details
    ctx['target_ticket'] = target_ticket
    ctx['ticket'] = ticket
    ctx['comments'] = reversed(comments)