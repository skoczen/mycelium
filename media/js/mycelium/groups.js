$(function(){
	$(".datepicker").datepicker({
	    numberOfMonths: 2,
	    showButtonPanel: true,
	    showCurrentAtPos: 1            
	});
	$(".group_delete_btn").click(delete_group);	
	$(".add_new_rule_btn").click(add_rule_row);
	$(".remove_rule_btn").click(remove_rule_row);
});
function remove_rule_row(target) {
	btn = $(this)
	rule = btn.parents("rule");
	$("input[name$=-right_side_type]",rule).val("");
	$("input[name$=-right_side_value]",rule).val("");
	$("select",rule).val("");
	$("textarea",rule).val("");
		$("input[name$=-DELETE]",rule).val("checked").attr("checked","checked");
	$("#basic_info_form").genericFieldForm('queue_form_save');
	rule.hide();
	$(".add_new_rule_btn").show();
	return false;
}
function add_rule_row() {
	$("rules rule:not(:visible):first").show().css("display","block");
	if ($("rules rule:not(:visible)").length == 0) {
		$(".add_new_rule_btn").hide();
	}
	return false;
}

function delete_group(e) {
    var name = $("#container_id_name .view_field").text();
    if (name == " ") {
        name = "Unnamed Group";
    }
    if (confirm("Are you sure you want to completely delete " + name + " from the database? \n\nDeleting will remove this group. It will affect any of the people in the group.\n\nIt cannot be undone.\n\nPress OK to delete "+ name +".\nPress Cancel to leave things unchanged.")) {
        $(window).unbind("unload.genericFieldForm");
        $("#delete_group_form").submit();
    }
    return false;
}

