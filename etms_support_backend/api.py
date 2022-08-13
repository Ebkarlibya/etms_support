from os import error
import site
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from etms_support_backend.auth import verify_request
import frappe
from frappe import _
from frappe.frappeclient import FrappeClient

@frappe.whitelist(allow_guest=False, methods=["POST"])
@verify_request
def get_tickets():
    frappe.only_for(["ETS Support Moderator", "ETS Support User"])

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
            "description"
        ],
        filters=fdict)
    
    return tickets

@frappe.whitelist(allow_guest=False, methods=["POST"])
def get_ticket():
    frappe.only_for(["ETS Support Moderator", "ETS Support User"])

    roles = frappe.get_roles()
    ticket_name = frappe.form_dict["ticket_name"]
    ticket = frappe.get_doc("Issue", ticket_name)

    if ticket.raised_by != frappe.session.user and not "ETS Support Moderator" in roles:
        return {"message": "not allowed"}
    user_details = frappe.get_all("User", fields=["full_name", "user_image"], filters={
        "name": ticket.raised_by
    })[0]

    # attachments = frappe.get_all("File", fields="file_url", filters={
    #     "attached_to_doctype": "Issue",
    #     "attached_to_name": ticket.name
    # })
    
    # for idx, att in enumerate(attachments):
    #     attachments[idx].file_url = urljoin(ctx.url, att.file_url)
    # if len(attachment_path) > 0:
    #     ctx['attachment_url'] = urljoin(ctx.url, attachment_path[0].file_url)

    # append user name and image to each comment user
    _comments = frappe.get_all("Comment", 
        fields=["name", "creation", "comment_email", "content", "comment_type", "reference_doctype", "reference_name"], 
        filters={
        "reference_doctype": "Issue",
        "reference_name": ticket.name
    })
    # filter out (Added) comments
    # comments = list(filter(lambda c: c.comment_type == "Comment", _comments))
    attachments = []
    comments = []
    for _c in _comments:
        if _c.comment_type == "Comment":
            _c['user_details'] = frappe.get_all("User", 
            fields=["full_name", "user_image"],
            filters={"name": _c.comment_email})[0]

            # get the comment attachments
            comment_attachments = frappe.get_all("Comment", 
                fields=["creation", "comment_email", "content"], 
                filters={
                "reference_doctype": "Comment",
                "reference_name": _c.name
            })
            for idx, att in enumerate(comment_attachments):
                soup = BeautifulSoup(comment_attachments[idx].content).find("a")
                att_url = urljoin("http://google.com", soup.attrs.get("href"))
                comment_attachments[idx]['file_url'] = att_url
            _c['comment_attachments'] = comment_attachments
            comments.append(_c)
        # get the issue attachments
        elif _c.comment_type == "Attachment":
            soup = BeautifulSoup(_c.content).find("a")
            att_url = urljoin("http://google.com", soup.attrs.get("href"))
            _c['file_url'] = att_url
            attachments.append(_c)

    # attachments = list(filter(lambda c: c.comment_type == "Comment", _comments))

    # for comment in comments:
    #     comment['user_details'] = frappe.get_all("User", 
    #         fields=["full_name", "user_image"],
    #         filters={"name": comment.comment_email})[0]
    data = {}
    data['attachments'] = attachments
    data['comments'] = reversed(comments)
    data['user_details'] = user_details
    data['target_ticket'] = ticket_name
    data['ticket'] = ticket

    return data
    
@frappe.whitelist()
def create_ticket(subject, description, issue_type):
    frappe.only_for(["ETS Support Moderator", "ETS Support User"])

    # tconf = frappe.get_single("Tickets Settings")
    # depOptions = tconf._meta.fields[0].options.split('\n')
    
    ticket = frappe.new_doc("Issue")
    customer = frappe.db.get_value("Customer", filters={"name": frappe.session.user}, fieldname="name")
    ticket.issue_type = issue_type
    ticket.subject = subject
    ticket.description = description
    ticket.raised_by = frappe.session.user
    ticket.customer = customer
    # ticket.user_name = user.full_name
    # ticket.user_image = user.user_image
    
    ticket.insert()

    return {"message": "success"}

@frappe.whitelist()
def replay_ticket(ticket_name, replay_text):
    frappe.only_for(["ETS Support Moderator", "ETS Support User"])
    
    ticket = frappe.get_doc("Issue", ticket_name)

    if ticket.raised_by == frappe.session.user or "ETS Support Moderator" in frappe.get_roles():
        if ticket.status == "closed":
            return {"message": "Cant replay to a closed Ticket."}

        if "ETS Support User" in frappe.get_roles():
            ticket.status = "Open"
            ticket.save()

        if "ETS Support Moderator" in frappe.get_roles():
            ticket.status = "Replied"
            ticket.save()

        replay = frappe.new_doc("Comment")
        replay.comment_email = frappe.session.user
        replay.comment_type = "Comment"
        replay.reference_doctype = "Issue"
        replay.reference_name = ticket_name
        replay.content = replay_text

        replay.save()
        return {"message": "success"}

        # frappe.db.commit()
    return replay


@frappe.whitelist()
def close_ticket(ticket_name):
    frappe.only_for(["ETS Support Moderator", "ETS Support User"])
            
    try:
        ticket = frappe.get_doc("Issue", ticket_name)
        if ticket.raised_by == frappe.session.user or "ETS Support Moderator" in frappe.get_roles():
            ticket.status = "Closed"
            ticket.save()
        return {"message": "success"}
    except Exception as e:
        print(e)

    return ticket


