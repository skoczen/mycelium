$(function(){
	$(".spreadsheet_delete_btn").click(delete_spreadsheet);	
	$("#basic_info_form").submit(function(){return false;});
	$("#basic_info_form input").change(enable_disable_download_button);
	$("#basic_info_form select").change(enable_disable_download_button);
});


function delete_spreadsheet(e) {
    var name = $("#container_id_name .view_field").text();
    if (name == "") {
        name = "Unnamed Spreadsheet";
    }
    if (confirm("Are you sure you want to completely delete " + name + " from the database? \n\nDeleting will remove this spreadsheet. It will affect any of the people in the spreadsheet.\n\nIt cannot be undone.\n\nPress OK to delete "+ name +".\nPress Cancel to leave things unchanged.")) {
        $(window).unbind("unload.genericFieldForm");
        $("#delete_spreadsheet_form").submit();
    }
    return false;
}

function form_changed() {
	// copy the values to the hidden submit fields.. ?
	enable_disable_download_button();
}
function enable_disable_download_button() {
	if ($("input[name=default_filetype]").val() != "" && $("input[name=spreadsheet_template]").val() != "" && $("input[name=group]").val() != "" )	{
		$(".do")
	}
}