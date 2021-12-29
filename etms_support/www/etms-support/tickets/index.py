import frappe
from frappe import data_migration

def get_context(ctx):
    ctx.no_cache = 1
    user = frappe.get_doc("User", frappe.session.user)
    fdict = {}
    if not user.name == "Administrator":
        fdict['user'] = user.name

    tickets = frappe.get_all(
        "Tickets",
        fields=[
            "name",
            "creation",
            "department",
            "subject",
            "description",
            "status"
        ], filters=fdict)

    ctx['company'] = frappe.defaults.get_user_default("Company")
    ctx['tickets'] = tickets