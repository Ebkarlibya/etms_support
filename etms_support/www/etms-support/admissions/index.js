var siteFilter = document.querySelector("#etms-search-filters-site");
var approvalStatusFilter = document.querySelector("#etms-search-filters-approval-status");
var actionStatusFilter = document.querySelector("#etms-search-filters-action-status");
var clearFilters = document.querySelector(".etms-clear-filters");
var admissions_table;


siteFilter.onchange = function(e) {
    var site_name = e.target.value;

    if(site_name != "none") {
        console.log(site_name);
        admissions_table.columns(0).search(site_name);
        admissions_table.columns(0).draw();
    } else {
        admissions_table.columns(0).search("");
        admissions_table.columns(0).draw();
    }
}

approvalStatusFilter.onchange = function(e) {
    var status = e.target.value;

    if(status != "none") {
        admissions_table.columns(1).search(status);
        admissions_table.columns(1).draw();
    } else {
        admissions_table.columns(1).search("");
        admissions_table.columns(1).draw();
    }
}
actionStatusFilter.onchange = function(e) {
    var status = e.target.value;

    if(status != "none") {
        admissions_table.columns(2).search(status);
        admissions_table.columns(2).draw();
    } else {
        admissions_table.columns(2).search("");
        admissions_table.columns(2).draw();
    }
}
clearFilters.addEventListener('click', function() {
    admissions_table.columns(0).search("").draw();
    admissions_table.columns(1).search("").draw();
    admissions_table.columns(2).search("").draw();
    siteFilter.value = "none";
    approvalStatusFilter.value = "none";
    actionStatusFilter.value = "none";
});

admissions_table = new DataTable('#tickets-table',{
    paging:   true,
    ordering: false,
    info:     true,
    autoWidth : true,
    responsive: false,
    pageLength: 10,
    search: true,
    language: {
        search: "",
        searchPlaceholder: frappe._("Related Site"),
                    stateRestore: {
            creationModal:{
                search: 'Searching:'
            }
        },
        emptyTable: document.querySelector("meta[name='nodata_translation']").content, 
        paginate: {
            next: document.querySelector("meta[name='next_translation']").content,
            previous: document.querySelector("meta[name='previous_translation']").content
        }
    }
});

admissions_table.table().container().classList.remove('form-inline');
document.querySelector("#tickets-table_length").parentElement.parentElement.remove();
document.querySelector("#tickets-table_info").remove();
document.querySelector("#tickets-table").style.visibility = "";
