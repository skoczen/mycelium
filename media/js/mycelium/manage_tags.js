$(function() {
	$(".delete_tagset_btn").click(delete_category);
	$(".delete_tag_btn").click(delete_tag);
	$(".edit_tagset_name_btn").click(toggle_name_edit);
    $("form.category_name").genericFieldForm();
});
function delete_category() {
	var ts = $(this).parents("tagset");
	var tagset_row = $(".detail_header",ts);
	var tag_rows = $(".tag_row",ts);
	tagset_row.addClass("pre_delete");
	tag_rows.addClass("pre_delete");
	if (confirm("Hold on there.\n\nThis will delete the entire tag category, including all tags in it!\n\nThis action can not be undone.\n\nPress OK to delete this tag category.\nPress Cancel to leave it intact.")) {
		$.ajax({
			url: $(this).attr("href"),
			type: "POST",
			dataType: "json",
			success: function(json) {
				process_fragments_and_rebind_tags_form(json);
			}
		});	
	} else {
		tagset_row.removeClass("pre_delete");
		tag_rows.removeClass("pre_delete");
	}
	return false;
}
function delete_tag() {
	var tag_row = $(this).parents(".tag_row");
	tag_row.addClass("pre_delete");
	if (confirm("You sure?\n\nPress OK to delete this tag.\nPress Cancel to leave it in place.")) {
		$.ajax({
			url: $(this).attr("href"),
			type: "POST",
			dataType: "json",
			success: function(json) {
				process_fragments_and_rebind_tags_form(json);
			}
		});	
	} else {
		tag_row.removeClass("pre_delete");
	}
	return false;
}
function toggle_name_edit() {
	$(this).parents("tagset").toggleClass("edit_mode_on");
	return false;
}

function process_fragments_and_rebind_tags_form(json) {
    $.Mycelium.fragments.process_fragments_from_json(json);
    bind_tags_tab_events();
}
