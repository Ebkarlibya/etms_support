from ast import arg
from functools import wraps
import imp
from etms_support_backend.utils import log_error
import frappe
from frappe.core.doctype.user.user import User, test_password_strength

from frappe.utils import random_string

settings = frappe.get_single("ETS Settings")


def verify_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        headers = frappe.request.headers
        if settings.enabled == 0:
            return {"message": "services_disabled"}
        try:
            func_res = func()
            API_KEY = headers["Consumer-Key"]
            API_SECRET = headers["Consumer-Secret"]

            if API_KEY != settings.api_key or API_SECRET != settings.get_password(
                    "api_secret"):
                return {"message": "not_authorized"}
                # raise Exception('Some Error')
            # del kwargs['cmd']
            return func_res

        except Exception as e:
            log_error()
            print(frappe.get_traceback())
            print(e.args)
            return {"message": "internal_server_error"}

    return wrapper


@frappe.whitelist(allow_guest=True, methods=["POST"])
@verify_request
def login():
    usr = frappe.form_dict["usr"]
    pwd = frappe.form_dict["pwd"]

    try:
        if usr and pwd:
            _user = User.find_by_credentials(usr, pwd)
            user = frappe.get_doc("User", _user.name)
            if user and _user["is_authenticated"]:
                customer_not_verified = frappe.get_value("Customer",
                    fieldname="ets_is_customer_email_verified",
                    filters={"name": user.name})
                if customer_not_verified == 0:
                    return {"message": "user_email_not_verified"}

                return {
                    "message": "success",
                    "user": user.name,
                    "api_key": user.api_key,
                    "api_secret": user.get_password("api_secret"),
                }
            return {"message": "faild_to_login"}

    except Exception as e:
        log_error()
        return {"message": "faild_to_login"}

@frappe.whitelist(allow_guest=True, methods=["POST"])
@verify_request
def request_password_reset():
    email = frappe.form_dict["user_login"]

    user_exist = frappe.db.get_value("User", email)

    if user_exist:
        user = frappe.get_doc("User", email)

        next_reset_key = random_string(25)
        user.reset_password_key = next_reset_key
        reset_url = settings.domain + "/password-reset?key=" + next_reset_key

        user.flags.ignore_permissions = True
        user.save()

        # frappe.sendmail(
        #     recipients=[email],
        #     sender="notifications@torous.ly",
        #     subject="Torous: Password Reset",
        #     reply_to="notifications@torous.ly",
        #     expose_recipients=True,
        #     template="reset_password",
        #     args={
        #         "reset_url": reset_url
        #     },
        #     delayed=False
        # )
        return {"message": "password_reset_request_accepted"}
    else:
        return {"message": "password_reset_request_accepted"}

# no consumer keys (web browser request)
@frappe.whitelist(allow_guest=True, methods=["POST"])
def handle_password_reset():
    reset_key = frappe.form_dict["resetKey"]
    new_password = frappe.form_dict["newPassword"]
    
    reset_user_exist = frappe.db.get_value("User", filters={"reset_password_key": reset_key})

    pwTest = test_password_strength(new_password=new_password)
    pass_policy = pwTest.get("feedback").get("password_policy_validation_passed")

    if pass_policy == False:
        return {"message": "password_weak"}

    # log the try
    log_error(content=f"""
        Reset Key: {reset_key}
        New Password: {new_password}
        Pass Policy: {pass_policy}
    """)

    if reset_user_exist:
        user = frappe.get_doc("User", reset_user_exist)

        user.new_password = new_password
        user.reset_password_key = None
        
        # Generate new api keys
        api_secret = frappe.generate_hash(length=15)
        api_key = frappe.generate_hash(length=15)

        user.api_key = api_key
        user.api_secret = api_secret
        
        user.flags.ignore_permissions = True
        user.save()

        return {"message": "password_reset_accepted"}
    else:
        return {"message": "password_reset_rejected"}

@frappe.whitelist(allow_guest=True, methods=["GET"])
@verify_request
def request_confirmation_email():
    email = frappe.form_dict["email"]

    user_exist = frappe.db.get_value("User", filters={"name": email})
    
    if user_exist:
        customer = frappe.get_doc("Customer", user_exist)
        if customer.ets_is_customer_email_verified:
            return {"message": "faild"}

        confirmation_key = random_string(25)
        customer.ets_email_confirmation_key = confirmation_key

        customer.flags.ignore_mandatory = True
        customer.flags.ignore_permissions = True
        customer.save()

        confirm_url = settings.domain + "/eci-confirm-email?key=" + confirmation_key

        frappe.sendmail(
            recipients=[email],
            sender="notifications@torous.ly",
            subject="Torous: Confirm Your Email",
            reply_to="notifications@torous.ly",
            expose_recipients=True,
            template="confirm_email",
            args={
                "confirm_url": confirm_url
            },
            delayed=False
        )
        return {"message": "confirmation_email_sent"}
    else:
        return {"message": "faild"}

# @frappe.whitelist(allow_guest=True, methods=["POST"])
# def sign_up():
#     if frappe.get_value("ECI Commerce Settings",
#                         fieldname="allow_new_users_registrations") == 0:
#         return {"message": "new_registrations_disabled"}

#     username = frappe.form_dict["username"]
#     new_password = frappe.form_dict["new_password"]
#     first_name = frappe.form_dict["first_name"]
#     last_name = frappe.form_dict["last_name"]
#     phone_number = frappe.form_dict["phone_number"]
#     phone_number2 = frappe.form_dict["phone_number2"]
#     shipping_city = frappe.form_dict["shipping_city"]
#     shipping_address_1 = frappe.form_dict["shipping_address_1"]

#     user_exist = frappe.db.get("User", username)

#     if user_exist:
#         customer_not_verified = frappe.get_value("Customer",
#             fieldname="eci_is_customer_email_verified",
#             filters={"name": user_exist.name})
#         if customer_not_verified == 0:
#             return {"message": "user_email_not_verified"}

#         return {"message": "user_already_exist"}

#     if frappe.db.get_creation_count('User', 60) > 300:
#         return {
#             "message":
#             "Too many users signed up recently, so the registration is disabled. Please try back in an hour"
#         }

#     user = frappe.get_doc({
#         "doctype": "User",
#         "email": username,
#         "first_name": first_name,
#         "enabled": 1,
#         "new_password": new_password,
#         "last_name": last_name,
#         "user_type": "Website User"
#     })

#     # Generate api keys
#     api_secret = frappe.generate_hash(length=15)
#     api_key = frappe.generate_hash(length=15)

#     user.api_key = api_key
#     user.api_secret = api_secret

#     user.flags.ignore_permissions = True
#     user.flags.ignore_password_policy = True

#     user.send_welcome_email = False
    
#     user.insert()
#     user.add_roles("Customer")
#     # user.save()

#     frappe.set_user("administrator")
#     customer = frappe.get_doc({
#         "doctype": "Customer",
#         "account_manager": user.name,
#         "customer_name": user.email,
#         "customer_group": "Commercial",
#         "territory": "All Territories",
#         "customer_type": frappe._("Individual"),
#         "mobile_no": phone_number,
#         "eci_mobile_no_2": phone_number2,
#         "default_price_list": settings.default_signup_customer_price_list
#     })
    
#     # generate confirmation key
#     confirmation_key = random_string(25)
#     customer.eci_email_confirmation_key = confirmation_key

#     # new customer
#     customer.flags.ignore_mandatory = True
#     customer.flags.ignore_permissions = True
#     customer.insert(ignore_permissions=True)

#     # new address
#     new_address = frappe.get_doc({
#         "doctype": "Address",
#         "address_title": user.name,
#         "address_type": "Shipping",
#         "address_line1": shipping_address_1,
#         "city": shipping_city,
#         "country": "Libya",
#         "email_id": user.email,
#         "phone": user.mobile_no,
#         "links": [
#             {
#                 "link_doctype": "Customer",
#                 "link_name": user.namepc
#             }
#         ]
#     })

#     new_address.flags.ignore_mandatory = True
#     new_address.flags.ignore_permissions = True
#     new_address.insert()


#     confirm_url = settings.eci_domain + "/eci-confirm-email?key=" + confirmation_key

#     # frappe.sendmail(
#     #     recipients=[user.email],
#     #     sender="notifications@torous.ly",
#     #     subject="Torous: Confirm Registration",
#     #     reply_to="notifications@torous.ly",
#     #     expose_recipients=True,
#     #     template="confirm_email",
#     #     args={
#     #         "confirm_url": confirm_url
#     #         },
#     #     delayed=False
#     # )

#     return {"message": "registered_successfully"}
    
#     # return {"user": user.name, "api_key": api_key, "api_secret": api_secret}



# @frappe.whitelist(allow_guest=False, methods=["GET"])
# @verify_request
# def user_info():
#     user = frappe.get_doc("User", frappe.session.user)

#     address_line1 = frappe.db.get_value(
#         "Address",
#         filters={"name": f"{user.name}-Shipping"},
#         fieldname="address_line1")
#     city = frappe.db.get_value("Address",
#                                filters={"name": f"{user.name}-Shipping"},
#                                fieldname="city")
#     info = {
#         "id": user.name,
#         "name": user.name,
#         "displayname": user.full_name,
#         "username": user.username,
#         "email": user.email,
#         "firstname": user.first_name,
#         "lastname": user.last_name,
#         "nicename": user.first_name,
#         "avatar": user.user_image,
#         "url": "",
#         "roles": [],
#         "address_line1": address_line1,
#         "city": city
#     }

#     return info