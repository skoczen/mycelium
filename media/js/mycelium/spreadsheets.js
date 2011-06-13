$(function(){
	$(".spreadsheet_delete_btn").click(delete_spreadsheet);	
	$("#basic_info_form").submit(function(){return false;});
	$("#basic_info_form input").change(form_changed);
	$("#basic_info_form select").change(form_changed);
	$(".file_type_option input").change(file_type_option_clicked);
	$("#container_id_spreadsheet_template input").change(template_type_changed);
	$("#basic_info_form").bind("genericFieldForm.save_form_success",form_saved);
});

var group_id = false;
var template_type = false;

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
	
	var new_group_id = $("#id_group").val();
	var new_template_type = $(".file_type_option input:checked").val()
	


	if (group_id != new_group_id) {
		update_group_count();
	}

	var changed =  (group_id != new_group_id || new_template_type != template_type );
	group_id = new_group_id;
	template_type = new_template_type;

	if (changed && new_template_type == "email_list") {
		$("fragment[name=email_quick_copy] textarea").html("Loading...");
	}
}

function form_saved() {
	update_email_list();
}

function file_type_option_clicked() {
	var selected = $(this);
	var container = selected.parents(".selects_with_descriptions");
	$(".file_type_option", container).removeClass("selected");
	selected.parents(".file_type_option").addClass("selected");
}

function template_type_changed() {
	var input = $(this);
	if (input.val() == "email_list") {
		$(".email_quick_copy").show().removeClass("hidden");
	} else {
		$(".email_quick_copy").hide();
	}

	// check if email needs updated
}
function update_email_list(){
	now = new Date().getTime();
	$.ajax({
          url: $("fragment[name=email_quick_copy]").attr("url") + "?" + now,
          type: "GET",
          dataType: "json",
          data: {},
          mode: 'abort',
          port: "email_list",
          success: function(json) {
            if (typeof(json) == typeof({})) {
				$.Mycelium.fragments.process_fragments_from_json(json);
             }
          }
     });
}
function update_group_count(){
	$("fragment[name=group_count] textarea").html("");
	now = new Date().getTime();
	$.ajax({
          url: $("fragment[name=group_count]").attr("url") + "?" + now,
          type: "GET",
          dataType: "json",
          data: {"group_id":$("#id_group").val()},
          mode: 'abort',
          port: "group_count",
          success: function(json) {
            if (typeof(json) == typeof({})) {
				$.Mycelium.fragments.process_fragments_from_json(json);
             }
          }
     });
}