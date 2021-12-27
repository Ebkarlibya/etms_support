from os import error
import frappe


@frappe.whitelist()
def submit_ticket(departmentIndex, subject, description):
    user = frappe.get_doc("User", frappe.session.user)
    tconf = frappe.get_single("Tickets Settings")
    depOptions = tconf._meta.fields[0].options.split('\n')
    
    ticket = frappe.new_doc("Tickets")

    ticket.department = depOptions[int(departmentIndex)]
    ticket.subject = subject
    ticket.description = description,
    ticket.user_name = user.full_name
    ticket.user_image = user.user_image

    ticket.insert()

    return ticket

@frappe.whitelist()
def close_ticket(ticket_name):
    user = frappe.get_doc("User", frappe.session.user)
    # tconf = frappe.get_single("Tickets Settings")
    
    try:
        ticket = frappe.get_doc("Tickets", ticket_name)
        ticket.status = "Closed"
        ticket.save()

    except Exception as e:
        print(e)

    return ticket

@frappe.whitelist()
def submit_replay(ticket_name, replay_text):
    user = frappe.get_doc("User", frappe.session.user)
    tconf = frappe.get_single("Tickets Settings")
    
    ticket = frappe.get_doc("Tickets", ticket_name)
    if ticket.status == "closed":
        frappe.throw("Cant replay to a closed Ticket.")

    ticket.append("replays", {
        "message": replay_text,
        "user": user.name,
        "user_name": user.full_name,
        "user_image": user.user_image
    })

    ticket.save()
    frappe.db.commit()

    return ticket