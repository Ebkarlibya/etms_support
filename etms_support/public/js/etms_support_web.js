jQuery(document).ready(function() {
    var third_party_apps = document.querySelector("a[href='/third_party_apps']");
    if(third_party_apps) {
        third_party_apps.remove();
    }
    setTimeout(function(){
        var input_lang = document.querySelector("input[data-fieldname='language']");
        
        if(input_lang){
            var el = `<select class="lang-options form-control" style="margin-bottom: 10px">
            <option value="ar">العربية</option>
            <option value="en">English</option>
            </select>`
            
            // insert options element
            input_lang.insertAdjacentHTML("beforeBegin", el);
            
            // change language field when select field change
            var lang_options = input_lang.parentElement.querySelector(".lang-options");
            lang_options.onchange = function(e) {
                input_lang.value = e.target.value;
            }
            // set language selector to be the language main field value on load
            lang_options.value = input_lang.value;
            input_lang.style.display = "none";
        }        
    }, 1500);
})