$(function(){
    if (!("placeholder" in document.createElement("input"))) {
        $('#global_search').toggleVal({populateFrom:"custom", text:"Search for anything..."}).addClass("prefilled");
    }

    $("#global_search").myceliumSearch({
	    search_url: GLOBAL_SEARCH_URL,        
        search_element: $("#global_search"),
	    results_element: $("fragment[name=global_search_results]")
    });
    
    $("#global_search").bind("myceliumSearch.return_pressed",open_if_only_result);

});
function open_if_only_result(e) {
	if ($(".global_results_table.results_found").length == 1 && $(".global_results_table.results_found tr.result_row").length == 1) {
		document.location = $(".global_results_table.results_found tr.result_row td.name a").attr("href");
	}
}