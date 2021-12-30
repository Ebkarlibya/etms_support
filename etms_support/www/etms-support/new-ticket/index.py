import frappe
from frappe import data_migration

def get_context(ctx):
    ctx.no_cache = 1
    

    # issues types
    issue_types = frappe.get_all("Issue Type")
    ctx['issue_types'] = issue_types

    user = frappe.session.user
    
    ctx['user'] = user
