import frappe
from frappe import data_migration

def get_context(ctx):
    ctx.no_cache = 1
    frappe.only_for(["ETMS Support User"])


    user = frappe.get_doc("User", frappe.session.user)
    fdict = {}

    fdict['contact_email'] = user.name

    action_sites = frappe.get_all(
        "Action ON ERP Site",
        fields="*", filters=fdict)

    ctx['action_sites'] = action_sites