var aoes_approval_selector = document.querySelector("#customer_site_access_approval");
var aoes_confirm_title = document.querySelector("meta[name='aoes-confirm-title']").content;
var aoes_confirm_approve = document.querySelector("meta[name='aoes-confirm-approve']").content;
var aoes_confirm_reject = document.querySelector("meta[name='aoes-confirm-reject']").content;


aoes_approval_selector.onchange = function(e) {
    if(e.target.value != 'open') {
        alertify.confirm(aoes_confirm_title, function(){
            
        },
        function(){
            
        }).set('closable', false).set('labels', {ok: aoes_confirm_approve, cancel: aoes_confirm_reject}); 
    }
}