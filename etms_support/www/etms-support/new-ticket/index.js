var issues_types = document.querySelector("#etms-issues-types");
var subject = document.querySelector("#etms-subject");
var description = document.querySelector("#etms-description");
var attachFile = document.querySelector("#etms-attach-file");
var attachBtn =  document.querySelector('.etms-attach-btn');
var submitTicket = document.querySelector("#etms-submit-ticket");
var alertSuccess = document.querySelector(".alert-success");
var alertError = document.querySelector(".alert-danger");

attachBtn.addEventListener('click', function(e) {
    if(attachFile.files[0]) {
        attachFile.value = null;
        attachBtn.classList.remove('btn-warning');
        attachBtn.classList.add('btn-default');
        return;    
    }
    attachFile.click();
})
attachFile.onchange = function(e) {
    console.log();
    if(e.target.files[0]) {
        attachBtn.classList.remove('btn-default');
        attachBtn.classList.add('btn-warning');
    } else {
        attachBtn.classList.remove('btn-warning');
        attachBtn.classList.add('btn-default');
    }
}

// Submit ticket
submitTicket.addEventListener("click", function () {
    var issue_type = issues_types.value;
    var subj = subject.value;
    var desc = description.value;
    var file = attachFile.files[0];
    if (issue_type && subject && desc) {
        submitTicket.disabled = true;
        frappe.call({
            method: 'etms_support.tickets.submit_ticket',
            args: { issue_type: issue_type, subject: subj, description: desc },
            callback: async function (r) {
                console.log(r.message);
                if (r.message.name) {
                    let ticket_name = r.message.name;
                    if (file) {
                        var r = await upload_file(file, "Issue", ticket_name);
                    }
                    if(etms_recorder.recorded_file) {
                        var r2 = await upload_file(etms_recorder.recorded_file.data, "Issue", ticket_name);
                    }
                    console.log(r);
                    alertError.hidden = true;
                    alertSuccess.hidden = false;
                    alertSuccess.innerHTML = "Your Ticket: " + ticket_name + " Submitted, Thank you!";
                    setTimeout(function () {
                        location.href = "/etms-support/tickets";
                    }, 1500);
                } else {
                    alertError.hidden = false;
                    alertError.innerHTML = "Could not submit your ticket, please try again.";
                }
                // submitTicket.disabled = false;
            }
        })

    } else {
        alertError.hidden = false;
        alertError.innerHTML = "All fields required.";
    }
});



var playBtn = document.querySelector(".etms-play-btn");
var recBtn = document.querySelector(".etms-record-btn");
var trashBtn = document.querySelector(".etms-trash-btn");
var recordLink = document.querySelector(".etms-audio-recorder .help-box");
var recTimer = document.querySelector(".etms-recorder-timer");
var spinner = document.querySelector(".etms-spinner");

var isRecording = false;
var isPlaying = false;
var player = new Audio(""); // media player
var rec;
const MAX_RECORDING_TIME = 180

frappe.provide("etms_recorder");
etms_recorder = Object();
etms_recorder.durFormat = function (time) {
    var mins = Math.floor(time / 60);
    if (mins < 10) {
        mins = '0' + String(mins);
    }
    var secs = Math.floor(time % 60);
    if (secs < 10) {
        secs = '0' + String(secs);
    }

    return mins + ':' + secs;
}

// Play Button
playBtn.addEventListener("click", async function () {
    if (!etms_recorder.recorded_file) return;

    if (isPlaying) {
        isPlaying = false
        clearInterval(etms_recorder.playTask);
        etms_recorder.player.pause();
        etms_recorder.player.currentTime = 0;
        trashBtn.disabled = false;
        playBtn.children[0].classList.remove("bi-stop-fill");
        playBtn.children[0].classList.add("bi-play-fill");
        return;
    }
    isPlaying = true;
    trashBtn.disabled = true;

    const play_url = URL.createObjectURL(etms_recorder.recorded_file.data)
    etms_recorder.player = new Audio(play_url);

    etms_recorder.player.ondurationchange = function (a) {  
        if (typeof a.target.duration === "number" && a.target.duration !== Infinity) {
            etms_recorder.duration = etms_recorder.durFormat(a.target.duration);
            // recTimer.innerText = etms_recorder.durFormat(a.target.duration);
        }
    }
    etms_recorder.player.onended = function (a) {
        isPlaying = false;
        playBtn.disabled = false;
        trashBtn.disabled = false;
        recTimer.hidden = true;
        recTimer.innerText = "";
        playBtn.children[0].classList.remove("bi-stop-fill");
        playBtn.children[0].classList.add("bi-play-fill");
        console.log('clear play task', etms_recorder.playTask);
        clearInterval(etms_recorder.playTask);
    }
    try {
        await etms_recorder.player.play();
        etms_recorder.seconds = 0;
        etms_recorder.playTask = setInterval(function () {
            etms_recorder.seconds++;
            if (etms_recorder.duration) {
                recTimer.innerText = etms_recorder.durFormat(etms_recorder.seconds) + " / " + etms_recorder.duration;
            } else {
                recTimer.innerText = etms_recorder.durFormat(etms_recorder.seconds);
            }
        }, 1000);
        recTimer.hidden = false;
        playBtn.children[0].classList.remove("bi-play-fill");
        playBtn.children[0].classList.add("bi-stop-fill");

    } catch (e) {
        frappe.throw(e.message)
    }

});
// Record Button
recBtn.addEventListener("click", async function () {
    try {
        let stream = await navigator.mediaDevices.getUserMedia({ audio: true });

        // initialize if not
        if (!rec) {
            rec = new MediaRecorder(stream);
            rec.ondataavailable = function (e) {
                if (rec.state == "inactive") {
                    etms_recorder.recorded_file = e;
                    playBtn.hidden = false;
                    recBtn.hidden = true;
                    trashBtn.hidden = false;
                }

            }
        }
        // start recording
        if (!isRecording) {
            isRecording = true;
            rec.start();
            // update ui
            recBtn.style.backgroundColor = "red";
            recTimer.hidden = false;
            etms_recorder.recSeconds = 0;
            etms_recorder.recTask = setInterval(function () {
                if (etms_recorder.recSeconds >= MAX_RECORDING_TIME) {
                    isRecording = false;
                    rec.stop()
                    recBtn.style.backgroundColor = "white";
                    recTimer.hidden = true
                    clearInterval(etms_recorder.recTask)
                }
                etms_recorder.recSeconds++;
                recTimer.innerText = etms_recorder.durFormat(etms_recorder.recSeconds) + " / " + (MAX_RECORDING_TIME / 60).toFixed(2) + " min";

            }, 1000);
            frappe.show_alert(frappe._("Recording Started!"), 3)
        } else {
            isRecording = false;
            rec.stop()
            recBtn.style.backgroundColor = "white";
            recTimer.hidden = true
            clearInterval(etms_recorder.recTask)
        }

    } catch (e) {
        frappe.msgprint(frappe._("Please Allow Microphone Access."))
    }
});
// Trash Button
trashBtn.addEventListener("click", async function () {

    if (etms_recorder.recorded_file) {
        console.log('trash');
        playBtn.hidden = true;
        recBtn.hidden = false;
        trashBtn.hidden = true;
        etms_recorder.recorded_file = undefined;
    }

});

function upload_file(file, doctype, docname, name) {
    return new Promise(function (resolve, reject) {

        var xhr = new XMLHttpRequest();
        var fd = new FormData();
        var base_url = window.location.origin
        var file_name;
        if(!file.name) {
            file_name = "etms-support-" + docname + "-" + "record.webm";
        } else {
            file_name = "etms-support-" + docname + "-" + file.name;
        }
        var file_url = base_url + "/private/files/" + file_name;
        
        xhr.open("POST", "/api/method/upload_file", true);
        
        xhr.setRequestHeader("X-Frappe-CSRF-Token", frappe.csrf_token);
        xhr.setRequestHeader("ContentType", "Application/json");
        
        fd.append("file", file, file_name);
        fd.append("is_private", 1);
        fd.append("file_name", file_name);
        fd.append("file_url", file_url);
        if (doctype && docname) {
            fd.append("doctype", doctype);
            fd.append("docname", docname);
        }
        debugger
        xhr.send(fd);

        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4 && xhr.status == 200) {
                try {
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