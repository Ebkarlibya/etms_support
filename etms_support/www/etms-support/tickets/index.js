var siteFilter = document.querySelector("#etms-search-filters-site");
var statusFilter = document.querySelector("#etms-search-filters-status");
var clearFilters = document.querySelector(".etms-clear-filters");
var issues_table;


siteFilter.onchange = function(e) {
    var site_name = e.target.value;

    if(site_name != "none") {
        issues_table.columns(2).search(site_name);
        issues_table.columns(2).draw();
    } else {
        issues_table.columns(2).search("");
        issues_table.columns(2).draw();
    }
}

statusFilter.onchange = function(e) {
    var status = e.target.value;

    if(status != "none") {
        issues_table.columns(3).search(status);
        issues_table.columns(3).draw();
    } else {
        issues_table.columns(3).search("");
        issues_table.columns(3).draw();
    }
}
clearFilters.addEventListener('click', function() {
    issues_table.columns(1).search("").draw();
    issues_table.columns(2).search("").draw();
    siteFilter.value = "none";
    statusFilter.value = "none";
});

issues_table = new DataTable('#tickets-table',{
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

issues_table.table().container().classList.remove('form-inline');
document.querySelector("#tickets-table_length").parentElement.parentElement.remove();
document.querySelector("#tickets-table_info").remove();
document.querySelector("#tickets-table").style.visibility = "";
