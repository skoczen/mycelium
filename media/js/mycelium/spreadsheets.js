$(function(){
	$(".spreadsheet_delete_btn").click(delete_spreadsheet);	
	$("#basic_info_form").submit(function(){return false;});
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

