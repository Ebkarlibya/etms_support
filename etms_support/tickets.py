import frappe


@frappe.whitelist()
def submit_ticket(departmentIndex, subject, description):
    user = frappe.session.user
    tconf = frappe.get_single("Tickets Settings")
    depOptions = tconf._meta.fields[0].options.split('\n')
    
    ticket = frappe.new_doc("Tickets")

    ticket.department = depOptions[int(departmentIndex)]
    ticket.subject = subject
    ticket.description = description,
    ticket.user = user

    ticket.insert()

    return ticket