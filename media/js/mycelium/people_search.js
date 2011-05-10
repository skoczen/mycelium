(function($){
    if (!("placeholder" in document.createElement("input"))) {
        $('#id_search_query').toggleVal({populateFrom:"custom", text:"Type in a name, phone number, or email..."}).addClass("prefilled");
    }

    $("#id_search_query").myceliumSearch({
	    search_url: SEARCH_URL,        
        search_element: $("#id_search_query"),
	    results_element: $("fragment[name=main_search_results]")
    });
    
    $.Mycelium.update_stripes("fragment[name=main_search_results]");
    $("#id_search_query").bind("myceliumSearch.return_pressed",open_if_only_result);

});
function open_if_only_result(e) {
	if ($(".results_table").length == 1 && $(".results_table tr.result_row").length == 1) {
		document.location = $(".results_table tr.result_row td.name a").attr("href");
	}
}