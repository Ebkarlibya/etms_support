import frappe
from frappe import data_migration

def get_context(ctx):
    ctx.no_cache = 1
    tconf = frappe.get_single("Tickets Settings")

    # department options
    departments = tconf._meta.fields[0].options.split("\n")
    ctx['departments'] = departments

    user = frappe.session.user
    
    ctx['user'] = user
