import frappe


def log_error(content=None):
    tb = frappe.get_traceback()
    print(tb)
    # doc = {
    #     "doctype": "ECI Error Logs",
    #     "content": content or tb
    # }

    # log = frappe.get_doc(doc)
    # log.flags.ignore_permissions = True
    # log.insert()

@frappe.whitelist(allow_guest=True, methods=["GET"])
def get_minimum_client_version():
    ets_settings = frappe.get_single("ETS Settings")

    return ets_settings.minimum_client_version