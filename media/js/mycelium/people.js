$(function(){
	$('#id_search_query').toggleVal({populateFrom:"custom", text:"Type in a name, phone number, or email..."}).addClass("prefilled");
	$("#id_search_query").live("keydown",queue_searching);
	update_stripes();
	$("#id_search_query").bind('keyup', 'return', open_if_only_result);
});
var q;
var search_timeout;
function queue_searching() {
	clearTimeout(search_timeout);
	search_timeout = setTimeout(update_search, 50);
}
function update_search() {
	q = $("#id_search_query").val();
	$.ajax({
	  url: "{% url people:search_results %}",
	  type: "GET",
	  dataType: "json",
	  data: {'q':q},
	  mode: 'abort',
	  success: function(json) {
		$(".search_results").html(json.html);
		highlight_search_terms(q);
		update_stripes();
	 },
	});
}
function highlight_search_terms(q) {
	var space_queries = q.split(" ");
	highlight_regexes = [];
	for (var j in space_queries) {
		var q = space_queries[j];
		if (q != "") {
			highlight_regexes.push(new RegExp(q, "gi"));

			var dash_queries = q.split("-");
			if (dash_queries.length > 1) {
				for (var k in dash_queries) {
					if (dash_queries[k] != "") {
						highlight_regexes.push(new RegExp(dash_queries[k], "gi"));
					}
				}
			}
		}
	}
	$(".highlightable").each(function(){
		var text = $(this).text();
		for (var j in highlight_regexes) {
			text = text.replace(highlight_regexes[j], '<b>$&</b>')
		}
		$(this).html(text);
	});

}
function update_stripes() {
	$(".result_row:even").addClass("even");
	$(".result_row:odd").addClass("odd");
}
function open_if_only_result(e) {
	if ($(".results_table").length == 1 && $(".results_table tr.result_row").length == 1) {
		document.location = $(".results_table tr.result_row td.name a").attr("href");
	}
}