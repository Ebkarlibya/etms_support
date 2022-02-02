frappe.ui.form.on("Issue", {
	refresh: function(frm) {
		frm.add_custom_button(frappe._("View in Web Chat"), function() {
			window.open("/etms-support/ticket?name="+frm.doc.name, "_blank").focus();
		});

		if(!frappe.user_roles.includes("ETMS Support Admin")) {
					document.querySelector('.form-attachments').remove();
					document.querySelector('.comment-box').remove();
					document.querySelector('.form-footer').remove();
		}
		
	}
})