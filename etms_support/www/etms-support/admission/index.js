var aoes_approval_selector = document.querySelector("#customer_site_access_approval");
var issueField = document.querySelector("#issue");
var aoes_confirm_title_approve = document.querySelector("meta[name='aoes-confirm-title-approve']").content;
var aoes_confirm_title_reject = document.querySelector("meta[name='aoes-confirm-title-reject']").content;
var aoes_confirm_approve = document.querySelector("meta[name='aoes-confirm-approve']").content;
var aoes_confirm_reject = document.querySelector("meta[name='aoes-confirm-reject']").content;
var aoes_confirm_cancle = document.querySelector("meta[name='aoes-confirm-cancle']").content;

var aoes_docname = document.querySelector("#aoes_docname");

if(aoes_approval_selector){
    aoes_approval_selector.onchange = function(e) {
        if(e.target.value != 'Open') {
            var text = e.target.value == "Approved" ? aoes_confirm_title_approve : aoes_confirm_title_reject;
            alertify.confirm(text, function(){
                set_approval_status(e.target.value);
            }).set('closable', false).set('title', 'ETMS Support').set('labels', {
                label: 'AOES',
                ok: e.target.value == "Approved" ? aoes_confirm_approve : aoes_confirm_reject,
                cancel: aoes_confirm_cancle
            }); 
        }
    }
}

function set_approval_status(approval_status) {
    frappe.call({
        method: 'etms_support.tickets.set_approval_status',
        args: { "approval_status": approval_status, "docname": aoes_docname .value },
        callback: function (r) {
            frappe.show_alert(r.message);
            setTimeout(function(){
                location.reload();
            }, 1200);
        }
    })
}
if(issueField && issueField.value != "None") {
    issueField.style.color = "blue";
    issueField.style.cursor = "pointer";
    issueField.addEventListener("click", function() {
        ticketUrl = "/etms-support/ticket?name=" + this.value;
        window.open(ticketUrl, "_blank").focus();
    });
}