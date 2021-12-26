var department = document.querySelector("#etms-department");
var subject = document.querySelector("#etms-subject");
var description = document.querySelector("#etms-description");
var submitTicket = document.querySelector("#etms-submit-ticket");
var alertSuccess = document.querySelector(".alert-success");
var alertError = document.querySelector(".alert-danger");



// Submit ticket
submitTicket.addEventListener("click", function() {
    var dep = department.value;
    var subj = subject.value;
    var desc = description.value;

    if (dep && !isNaN(parseInt(dep)) && subject && desc) {
        submitTicket.disabled = true;
        frappe.call({
            method: 'etms_support.tickets.submit_ticket',
            args: { departmentIndex: dep, subject: subj, description: desc },
            callback: function(r) {
                console.log(r.message);
                if (r.message.name) {
                    let ticket_name = r.message.name;
                    alertSuccess.hidden = false;
                    alertSuccess.innerHTML = "Your Ticket: " + ticket_name + " Submitted, Thank you!";
                    setTimeout(function() {
                        location.href = "/etms-support/tickets";
                    }, 1500);
                } else {
                    alertError.hidden = false;
                    alertError.innerHTML = "Could not submit your ticket, please try again.";
                }
                // submitTicket.disabled = false;
            }
        })

    }
});