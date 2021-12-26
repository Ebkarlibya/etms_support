import frappe
from frappe import data_migration

def get_context(ctx):
    user = frappe.session.user
    query = frappe.request.query_string
    target_ticket = query.decode('utf-8').split("=")[1]
    
    ticket = frappe.get_all(
        "Tickets", [
            "name",
            "creation",
            "department",
            "subject",
            "description",
            "user",
            "status"
        ],
        filters={
            "name": target_ticket
        }
    )[0]

    ctx['target_ticket'] = target_ticket
    ctx['ticket'] = ticket