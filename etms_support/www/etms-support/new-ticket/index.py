import frappe
from frappe import data_migration

def get_context(ctx):
    ctx.no_cache = 1
    
    frappe.only_for(["ETMS Support Moderator", "ETMS Support User"])
    user = frappe.get_all("User", fields=["email", "full_name"], filters={"name": frappe.session.user})[0]
    lang = frappe.lang
    # get user sites
    sites = frappe.get_all("ETMS ERP Site", filters={
        "contact_email": user.email
    })
    if len(sites) < 1:
        frappe.msgprint(frappe._("You dont have any active site"))

    
    ctx['full_name'] = user.full_name or ""
    ctx['lang'] = lang
    ctx['sites'] = sites