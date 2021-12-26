var replayArea = document.querySelector("#etms-replay-textarea");
var submitReplay = document.querySelector("#etms-submit-replay");
var closeTicket = document.querySelector("#etms-close-ticket");
var alertSuccess = document.querySelector(".alert-success");
var alertError = document.querySelector(".alert-danger");



// Submit replay
submitReplay.addEventListener("click", function() {
    var replay_text = replayArea.value;

    if (replay_text) {
        submitReplay.disabled = true;
        var urlParams = new URLSearchParams(window.location.search);
        var ticket_name = urlParams.get('name');
        frappe.call({
            method: 'etms_support.tickets.submit_replay',
            args: { ticket_name: ticket_name, replay_text },
            callback: function(r) {
                if (r.message.name) {
                    let ticket_name = r.message.name;
                    alertSuccess.hidden = false;
                    alertSuccess.innerHTML = "Your Replay Submitted, Thank you!";
                    setTimeout(function() {
                        window.location.reload();
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

// Close ticket
submitReplay.addEventListener("click", function() {

});