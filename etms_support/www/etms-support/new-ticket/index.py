import frappe
from frappe import data_migration

def get_context(ctx):
    ctx.no_cache = 1
    
    frappe.only_for(["ETMS Support Moderator", "ETMS Support User"])
    lang = frappe.lang
    # issues types
    # issue_types = frappe.get_all("Issue Type")
    # ctx['issue_types'] = issue_types

    full_name = frappe.get_all("User", fields=["full_name"], filters={"name": frappe.session.user})[0].full_name or ""
    
    ctx['full_name'] = full_name
    ctx['lang'] = lang