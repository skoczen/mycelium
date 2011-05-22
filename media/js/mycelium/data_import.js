$(function(){
	$.Mycelium.update_stripes();
	$(".toggle_result_line_detail").click(toggle_result_details);
});

function toggle_result_details(){
	var btn = $(this);
	var row = btn.parents(".result_data_line");
	$(".import_fields_container", row).toggle();
	return false;
}