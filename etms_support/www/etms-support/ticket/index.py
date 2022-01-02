import frappe
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_context(ctx):
    ctx.no_cache = 1
    frappe.only_for(["ETMS Support Moderator", "ETMS Support User"])


    user = frappe.get_doc("User", frappe.session.user)
    query = frappe.request.query_string
    target_ticket = query.decode('utf-8').split("=")[1]
    
    ticket = frappe.get_doc("Issue", target_ticket)
    roles = frappe.get_roles(user.username)
    if ticket.raised_by != user.name and not "ETMS Support Moderator" in roles:
        frappe.throw("Not Allowed")
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
                att_url = urljoin(ctx.url, soup.attrs.get("href"))
                comment_attachments[idx]['file_url'] = att_url
            _c['comment_attachments'] = comment_attachments
            comments.append(_c)
        # get the issue attachments
        elif _c.comment_type == "Attachment":
            soup = BeautifulSoup(_c.content).find("a")
            att_url = urljoin(ctx.url, soup.attrs.get("href"))
            _c['file_url'] = att_url
            attachments.append(_c)

    # attachments = list(filter(lambda c: c.comment_type == "Comment", _comments))

    # for comment in comments:
    #     comment['user_details'] = frappe.get_all("User", 
    #         fields=["full_name", "user_image"],
    #         filters={"name": comment.comment_email})[0]

    ctx['attachments'] = attachments
    ctx['comments'] = reversed(comments)
    ctx['user_details'] = user_details
    ctx['target_ticket'] = target_ticket
    ctx['ticket'] = ticket