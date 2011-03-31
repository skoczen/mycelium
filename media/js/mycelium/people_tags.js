function bind_tags_tab_events() {
	$("tab_contents.people_tags_tab .tags_list").genericTags({'mode':'checkbox'});
	$("#new_category").ajaxForm({"success":process_fragments_and_rebind_tags_form,"dataType": 'json'});
	$("tabbed_box[name=add_a_category]").bind("mycelium.tabbed_box.opened",function(){
        $("#new_category input[name$=name]").focus();
    });
	$("#new_category .cancel_add_btn").live("click", cancel_add_category);
	$("tab_contents.people_tags_tab .delete_tagset_btn").click(delete_category);
	$("tab_contents.people_tags_tab .edit_tagset_name_btn").click(toggle_name_edit);
    $("form.category_name").genericFieldForm();
}
function cancel_add_category() {
    $("tabbed_box[name=add_a_category] tab_title").trigger("click");
    return false;
}
function delete_category() {
	if (confirm("Hold on there.\n\nThis will delete the entire tag category, including all tags in it!\n\nThis action can not be undone.\n\nPress OK to delete this tag category.\nPress Cancel to leave it intact.")) {
		$.ajax({
			url: $(this).attr("href"),
			type: "POST",
			dataType: "json",
			success: function(json) {
				process_fragments_and_rebind_tags_form(json);
			}
		});	
	}
	return false;
}
function toggle_name_edit() {
	var col = $(this).parents("column");
	$("#category_name",col).toggleClass("edit_mode_on");
	return false;
}

function process_fragments_and_rebind_tags_form(json) {
    $.Mycelium.fragments.process_fragments_from_json(json);
    bind_tags_tab_events();
}
