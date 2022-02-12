import frappe
from frappe import data_migration

def get_context(ctx):
    ctx.no_cache = 1
    frappe.only_for(["ETMS Support User"])


    user = frappe.get_doc("User", frappe.session.user)
    lang = frappe.lang
    fdict = {}
    roles = frappe.get_roles()

    if not "ETMS Support Moderator" in roles:
        fdict['customer_contact_email'] = user.name

    action_sites = frappe.get_all(
        "Action ON ERP Site",
        fields=[
            "name",
            "creation",
            "etms_erp_site",
            "customer_site_access_approval",
            "action_status",
            "site_access_purpose"
        ], filters=fdict)

    ctx['action_sites'] = action_sites