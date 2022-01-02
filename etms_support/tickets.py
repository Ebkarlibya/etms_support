from os import error
import frappe


@frappe.whitelist()
def submit_ticket(subject, description):
    user = frappe.get_doc("User", frappe.session.user)
    # tconf = frappe.get_single("Tickets Settings")
    # depOptions = tconf._meta.fields[0].options.split('\n')
    
    ticket = frappe.new_doc("Issue")

    # ticket.issue_type = issue_type
    ticket.subject = subject
    ticket.description = description
    ticket.raised_by = user.name
    # ticket.user_name = user.full_name
    # ticket.user_image = user.user_image

    ticket.insert()

    return ticket

@frappe.whitelist()
def close_ticket(ticket_name):
    user = frappe.get_doc("User", frappe.session.user)
    # tconf = frappe.get_single("Tickets Settings")
    
    try:
        ticket = frappe.get_doc("Issue", ticket_name)
        ticket.status = "Closed"
        ticket.save()

    except Exception as e:
        print(e)

    return ticket

@frappe.whitelist()
def submit_replay(ticket_name, replay_text):
    user = frappe.get_doc("User", frappe.session.user)
    # tconf = frappe.get_single("Tickets Settings")
    
    ticket = frappe.get_doc("Issue", ticket_name)
    if ticket.status == "closed":
        frappe.throw("Cant replay to a closed Ticket.")
    replay = frappe.new_doc("Comment")
    replay.comment_email = user.name
    replay.comment_type = "Comment"
    replay.reference_doctype = "Issue"
    replay.reference_name = ticket_name
    replay.content = replay_text


    # ticket.add_comment(text=replay_text)
    # ticket.append("replays", {
    #     "message": replay_text,
    #     "user": user.name,
    #     "user_name": user.full_name,
    #     "user_image": user.user_image
    # })

    replay.save()
    # frappe.db.commit()

    return replay