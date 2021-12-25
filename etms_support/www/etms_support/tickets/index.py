import frappe
from frappe import data_migration

def get_context(ctx):
    user = frappe.session.user
    tickets = frappe.get_all(
        "Tickets",
        fields=[
            "name",
            "creation",
            "department",
            "subject",
            "description",
            "status"
        ])
    
    ctx['tickets'] = tickets