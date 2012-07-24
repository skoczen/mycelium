$(function(){
	$(".spreadsheet_delete_btn").click(delete_spreadsheet);	
	$("#basic_info_form").submit(function(){return false;});
	$("#basic_info_form input").change(form_changed);
	$("#basic_info_form select").change(form_changed);
	$(".file_type_option input").change(file_type_option_clicked);
	$("#container_id_spreadsheet_template input").change(template_type_changed);
	$("#basic_info_form").bind("genericFieldForm.save_form_success",form_saved);
	$(".download_spreadsheet_btn").click(download_button_clicked);
	update_spreadsheet_download_link();
	group_id = get_group_id();
	template_type = get_template_type();
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

function get_group_id() {
	return $("#id_group").val();
}
function get_template_type() {
	return $(".file_type_option input:checked").val()
}
function get_spreadsheet_id() {
	return $("input[name=spreadsheet_pk]").val();
}
function get_file_type() {
	return $(".file_type.selects_with_descriptions input:checked").val()
}

function form_changed() {
	var new_group_id = get_group_id();
	var new_template_type = get_template_type();
	
	update_spreadsheet_download_link();

	if (group_id != new_group_id) {
		update_group_count();
	}

	var changed =  (group_id != new_group_id || new_template_type != template_type );
	group_id = new_group_id;
	template_type = new_template_type;

	if (changed && new_template_type == "email_list") {
		$("fragment[name=email_quick_copy] textarea").html("Loading...");
	}
	disable_download_button();
}

function form_saved() {
	enable_download_button();
	if (get_template_type() == "email_list") {
		update_email_list();
	}
}

function disable_download_button() {
	$(".download_spreadsheet_btn").addClass("disabled").html("Updating...");
}
function enable_download_button() {
	$(".download_spreadsheet_btn").removeClass("disabled").html("Generate Spreadsheet");
}

function download_button_clicked() {
	if ($(".download_spreadsheet_btn").hasClass("disabled")) {
		return false
	}
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
function update_spreadsheet_download_link() {
	var new_link = $(".download_spreadsheet_btn").attr("base_url");
	
	new_link = new_link + "?type=" + get_file_type() + "&spreadsheet_id=" + get_spreadsheet_id();
	$(".download_spreadsheet_btn").attr("href",new_link);
}