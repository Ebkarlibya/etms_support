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
                    alertError.innerHTML = "Could not submit your ticket, please try again.";
                    alertError.hidden = false;
                }
                // submitTicket.disabled = false;
            }
        })

    }
});

// Close ticket
closeTicket.addEventListener("click", async function() {

    submitReplay.disabled = true;
    closeTicket.disabled = true;
    const urlParams = new URLSearchParams(window.location.search);
    const ticket_name = urlParams.get('name');
    try {
        const res = await frappe.call({
            method: 'etms_support.tickets.close_ticket',
            args: { ticket_name: ticket_name },
            async: true
        });
        console.log(res);
        if (res.message.name) {
            alertSuccess.hidden = false;
            alertSuccess.innerHTML = "Your Ticket " + res.message.name + " Closed, Thank you!";
            setTimeout(function() {
                window.location.href = "/etms-support/tickets";
            }, 1500);
        } else {
            alertError.innerHTML = "Could not close your ticket, please try again.";
            alertError.hidden = false;
            console.log(res.message);
        }
    } catch (e) {
        alertError.hidden = false;
        alertError.innerHTML = "Could not close your ticket, please try again.";
        setTimeout(function() {
            window.location.reload();
        }, 1500);
    }

    
});