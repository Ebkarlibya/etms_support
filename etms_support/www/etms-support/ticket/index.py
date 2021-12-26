import frappe
from frappe import data_migration

def get_context(ctx):
    user = frappe.session.user
    query = frappe.request.query_string
    target_ticket = query.decode('utf-8').split("=")[1]
    
    ticket = frappe.get_doc("Tickets", target_ticket)

    ctx['target_ticket'] = target_ticket
    ctx['ticket'] = ticket