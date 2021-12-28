var department = document.querySelector("#etms-department");
var subject = document.querySelector("#etms-subject");
var description = document.querySelector("#etms-description");
var attachFile = document.querySelector("#etms-attach-file");
var submitTicket = document.querySelector("#etms-submit-ticket");
var alertSuccess = document.querySelector(".alert-success");
var alertError = document.querySelector(".alert-danger");



// Submit ticket
submitTicket.addEventListener("click", function() {
    var dep = department.value;
    var subj = subject.value;
    var desc = description.value;
    var file = attachFile.files[0];
    if (dep && !isNaN(parseInt(dep)) && subject && desc) {
        submitTicket.disabled = true;
        frappe.call({
            method: 'etms_support.tickets.submit_ticket',
            args: { departmentIndex: dep, subject: subj, description: desc },
            callback: async function(r) {
                console.log(r.message);
                if (r.message.name) {
                    let ticket_name = r.message.name;
                    if(file) {
                        var r = await upload_file(file, "Tickets", ticket_name);
                    }
                    console.log(r);
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


function upload_file(file, doctype, docname) {
    return new Promise(function(resolve, reject) {

        var xhr = new XMLHttpRequest();
        var fd = new FormData();
        var base_url = window.location.origin
        var file_name = "todo-rec-" + file.name;
        var file_url = base_url + "/private/files/" + file_name;
    
    
        xhr.open("POST", "/api/method/upload_file", true);
    
        xhr.setRequestHeader("X-Frappe-CSRF-Token", frappe.csrf_token);
        xhr.setRequestHeader("ContentType", "Application/json");
    
        fd.append("file", file, file.name);
        fd.append("is_private", 1);
        fd.append("file_name", file_name);
        fd.append("file_url", file_url);
        if(doctype && docname) {
            fd.append("doctype", doctype);
            fd.append("docname", docname);
        }
        xhr.send(fd);
    
        xhr.onreadystatechange = function () {
          if (xhr.readyState == 4 && xhr.status == 200) {
            try{
                var res = JSON.parse(xhr.response).message;
                    resolve(res);
            } catch {
                console.log('reject', res);
                reject(res)
            }
          } 
        };
    })
}