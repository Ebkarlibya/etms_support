frappe.ui.form.on("Action ON ERP Site", {
    refresh: function(frm) {
        frm.add_custom_button(frappe._("Login As Site Manager"), function(){
            frappe.call({
                method: "etms_support.tickets.aoes_get_site_sid",
                args: { docname: frm.doc.etms_erp_site, aoes_docname: frm.docname },
                callback: function(r) {
                    if(r.message) {
                        window.open( r.message, "_blank").focus();
                    }
                }
            })
        });
        if(frm.doc.customer_site_access_approval != "Approved" || frm.doc.action_status != "Open") {
            frm.custom_buttons['Login As Site Manager'][0].disabled = true;
        } 
    }
})