import frappe
from frappe import data_migration

def get_context(ctx):
    tconf = frappe.get_single("Tickets Settings")

    # department options
    departments = tconf._meta.fields[0].options.split("\n")
    ctx['departments'] = departments

    user = frappe.session.user
    
    ctx['user'] = user
