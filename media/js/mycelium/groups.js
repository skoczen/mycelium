$(function(){
	$(".datepicker").datepicker({
	    numberOfMonths: 2,
	    showButtonPanel: true,
	    showCurrentAtPos: 1            
	});
	$(".group_delete_btn").click(delete_group);	
	$(".add_new_rule_btn").click(add_rule_row);
	$(".remove_rule_btn").click(remove_rule_row);
	$("#basic_info_form").bind("genericFieldForm.save_form_success",rules_saved);
	$("#basic_info_form").bind("genericFieldForm.queue_form_save",rule_changed);

});
function remove_rule_row(target) {
	btn = $(this)
	rule = btn.parents("rule");
	$("input[name$=-right_side_type]",rule).val("");
	$("input[name$=-right_side_value]",rule).val("");
	$("select",rule).val("");
	$("textarea",rule).val("");
		$("input[name$=-DELETE]",rule).attr("checked","checked");
	$("#basic_info_form").genericFieldForm('queue_form_save');
	rule.addClass("empty");
	$(".add_new_rule_btn").show();
	return false;
}
function add_rule_row() {
	$("rules rule:not(:visible):first").removeClass("empty");
	if ($("rules rule:not(:visible)").length == 0) {
		$(".add_new_rule_btn").hide();
	}
	return false;
}
function rule_changed(){
	$("fragment[name=group_member_list]").html("<span class='loading_text'>Loading...</span>")
}
function rules_saved(){
	update_member_count();
}
function update_member_count(){
	$.ajax({
          url: $(".group_members.group_detail_column").attr("members_update_url"),
          type: "GET",
          dataType: "json",
          data: {},
          mode: 'abort',
          success: function(json) {
            if (typeof(json) == typeof({})) {
				$.Mycelium.fragments.process_fragments_from_json(json);
				$.Mycelium.update_stripes(".group_detail_column");
             }
          }
     });
}
function update_members(){
	
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

