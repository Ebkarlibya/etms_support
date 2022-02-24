import frappe
from frappe import data_migration

def get_context(ctx):
    ctx.no_cache = 1
    frappe.only_for(["ETMS Support Moderator", "ETMS Support User"])


    user = frappe.get_doc("User", frappe.session.user)
    lang = frappe.lang
    fdict = {}
    roles = frappe.get_roles()

    if not "ETMS Support Moderator" in roles:
        fdict['raised_by'] = user.name

    tickets = frappe.get_all(
        "Issue",
        fields=[
            "name",
            "creation",
            "status",
            "issue_type",
            "priority",
            "customer",
            "subject",
            "company",
            "raised_by",
            "description",
            "etms_erp_site"
        ], filters=fdict)
    sites = frappe.get_all("ETMS ERP Site", filters={
        "contact_email": user.email
    })
    ctx['company'] = frappe.defaults.get_user_default("Company")
    ctx['tickets'] = tickets
    ctx['lang'] = lang
    ctx['sites'] = sites