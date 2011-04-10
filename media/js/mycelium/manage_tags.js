$(function() {
    $("form.category_name").genericFieldForm();
    bind_tags_events();
});
function bind_tags_events() {
	$(".delete_tagset_btn").click(delete_category);
	$(".delete_tag_btn").click(delete_tag);
	$(".add_a_tag_btn").click(add_a_tag);
	$(".add_a_category_btn").click(add_a_category);
}

function process_link_via_json(t) {
	$.ajax({
		url: $(t).attr("href"),
		type: "POST",
		dataType: "json",
		success: function(json) {
			process_fragments_and_rebind_tags_form(json);
		}
	});
}

function delete_category() {
	var ts = $(this).parents("tagset");
	var tagset_row = $(".detail_header",ts);
	var tag_rows = $(".tag_row",ts);
	var ts_add = $(".add_a_tag_btn",ts);
	tagset_row.addClass("pre_delete");
	tag_rows.addClass("pre_delete");
	ts_add.addClass("pre_delete")
	if (confirm("Hold on there.\n\nThis will delete the entire tag category, including all tags in it!\n\nThis action can not be undone.\n\nPress OK to delete this tag category.\nPress Cancel to leave it intact.")) {
		process_link_via_json($(this));
	} else {
		tagset_row.removeClass("pre_delete");
		tag_rows.removeClass("pre_delete");
		ts_add.removeClass("pre_delete");
	}
	return false;
}
function delete_tag() {
	var tag_row = $(this).parents(".tag_row");
	tag_row.addClass("pre_delete");
	if (confirm("You sure?\n\nPress OK to delete this tag.\nPress Cancel to leave it in place.")) {
		process_link_via_json($(this));
	} else {
		tag_row.removeClass("pre_delete");
	}
	return false;
}
function add_a_tag() {
	process_link_via_json($(this));
	return false;
}
function add_a_category() {
	process_link_via_json($(this));
	return false;
}

function process_fragments_and_rebind_tags_form(json) {
    $.Mycelium.fragments.process_fragments_from_json(json);
    $.Mycelium.update_stripes();
    bind_tags_events();
}
