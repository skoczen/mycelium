$(function() {
    $("form.category_name").genericFieldForm();
    bind_tags_events();
});

var manageTags = {};
manageTags.state = {};
manageTags.objects = {};
manageTags.actions = {};
manageTags.handlers = {};
manageTags.ui = {};

manageTags.objects.tag = function() {};
manageTags.objects.tagSet = function() {};

manageTags.state.tags = [];
manageTags.state.tag_sets = [];

manageTags.handlers.add_tag_clicked = function() {};
manageTags.handlers.tag_name_changed = function() {};
manageTags.handlers.delete_tag_clicked = function() {};
manageTags.handlers.add_tagset_clicked = function() {};
manageTags.handlers.tagset_name_changed = function() {};
manageTags.handlers.delete_tagset_clicked = function() {};

manageTags.actions.add_tag = function() {};
manageTags.actions.update_tag = function() {};
manageTags.actions.delete_tag = function() {};
manageTags.actions.add_tagset = function() {};
manageTags.actions.update_tagset = function() {};
manageTags.actions.delete_tagset = function() {};

manageTags.ui.render_tag_row = function() {};
manageTags.ui.render_tagset = function() {};
manageTags.ui.render_full_ui = function() {};


function bind_tags_events() {
	$(".delete_tagset_btn").die("click").live("click",delete_category);
	$(".delete_tag_btn").die("click").live("click",delete_tag);
	$(".add_a_tag_btn").die("click").live("click",add_a_tag);
	$(".add_a_category_btn").die("click").live("click",add_a_category);
}

function process_link_via_json(t) {
	setTimeout(function(){
	if ($("#basic_info_form").hasClass("dirty")) {
		$("#basic_info_form").ajaxSubmit({
			'async':false
		});		
	}
	$.ajax({
		url: $(t).attr("href"),
		type: "POST",
		dataType: "json",
		success: function(json) {
			process_fragments_and_rebind_tags_form(json);
		}
	});
	},10);
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
