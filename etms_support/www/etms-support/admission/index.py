import frappe

def get_context(ctx):
    ctx.no_cache = 1
    frappe.only_for(["ETMS Support User"])


    # user = frappe.get_doc("User", frappe.session.user)

    query = frappe.request.query_string
    target_site_action = query.decode('utf-8').split("=")[1]
    
    action_on_erp_site = frappe.get_doc("Action ON ERP Site", target_site_action)

    if not action_on_erp_site.contact_email == frappe.session.user:
        frappe.throw("Not Allowed")

    ctx['aoes'] = action_on_erp_site