$(function(){
	$(".datepicker").datepicker({
	    numberOfMonths: 2,
	    showButtonPanel: true,
	    showCurrentAtPos: 1            
	});
	$(".group_delete_btn").click(delete_group);	
	$("rule").formset();
});

function delete_group(e) {
    var name = $("#container_id_name .view_field").text();
    if (name == " ") {
        name = "Unnamed Group";
    }
    if (confirm("Are you sure you want to completely delete " + name + " from the database? \n\nDeleting will remove this group. It will affect any of the people in the group.\n\nIt cannot be undone.\n\nPress OK to delete "+ name +".\nPress Cancel to leave things unchanged.")) {
        $(window).unbind("unload.genericFieldForm");
        $("#delete_group_form").submit();
    }
}

