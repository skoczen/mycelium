var rewrite = {};


////////////////////////////////////////////////////////////////////////////
//////////////////////////// MANAGEMENT ////////////////////////////////////
////////////////////////////////////////////////////////////////////////////

rewrite.manage = {};
rewrite.manage.state = {};
rewrite.manage.urls = {};
rewrite.manage.handlers = {};
rewrite.manage.actions = {};
rewrite.manage.ui = {};

rewrite.manage.init = function() {
	rewrite.manage.state.init();
	rewrite.manage.urls.init();
	rewrite.manage.handlers.init();
	rewrite.manage.actions.init();
	rewrite.manage.ui.init();
}
rewrite.manage.state.init = function(){};
rewrite.manage.urls.init = function(){};
rewrite.manage.handlers.init = function(){
	$(".new_page_link").live("click", rewrite.manage.handlers.show_new_page_for_section);
	$(".cancel_new_page_link").live("click", rewrite.manage.handlers.hide_new_page_for_section);
	$(".new_section_link").live("click", rewrite.manage.handlers.show_new_section);
	$(".cancel_section_link").live("click", rewrite.manage.handlers.hide_new_section);
	$(".new_post_link").live("click", rewrite.manage.handlers.show_new_post);
	$(".cancel_post_link").live("click", rewrite.manage.handlers.hide_new_post);
};
rewrite.manage.actions.init = function(){};
rewrite.manage.ui.init = function(){};

rewrite.manage.state.pages_and_sections_order_manifest = function() {
	var manifest = {}
	var order = 0;
	$("section").each(function(){
		manifest["section_" + $(this).attr("section_id") + "_order"] = order;
		order++;
	});
	$(".page").each(function(){
		var page_id = $(this).attr("page_id");
		manifest["page_" + page_id + "_order"] = order;
		manifest["page_" + page_id + "_section"] = $(this).parents("section").attr("section_id");
		order++;
	});
	return manifest;
}

rewrite.manage.handlers.pages_sorted = function(e, ui) {
	rewrite.manage.actions.save_section_and_page_sort_order()
}
rewrite.manage.handlers.save_section_and_page_response = function(json) {
	rewrite.manage.ui.show_saved_pages_message();
}
rewrite.manage.handlers.response_error = function() {
	alert("Error Saving.")
}

rewrite.manage.handlers.show_new_page_for_section = function() {
	var section = $(this).parents("section");
	$(".new_page_form",section).show();
	$(".new_page_link",section).hide();
	return false;
}
rewrite.manage.handlers.hide_new_page_for_section = function() {
	var section = $(this).parents("section");
	$(".new_page_form",section).hide();
	$(".new_page_link",section).show();
	return false;
}

rewrite.manage.handlers.show_new_section = function() {
	$(".new_section_form").show();
	$(".new_section_link").hide();
	return false;
}
rewrite.manage.handlers.hide_new_section = function() {
	$(".new_section_form").hide();
	$(".new_section_link").show();
	return false;
}

rewrite.manage.handlers.show_new_post = function() {
	$(".new_post_form").show();
	$(".new_post_link").hide();
	return false;
}
rewrite.manage.handlers.hide_new_post = function() {
	$(".new_post_form").hide();
	$(".new_post_link").show();
	return false;
}

rewrite.manage.actions.save_section_and_page_sort_order = function() {
	$.ajax({
		url: rewrite.manage.urls.save_page_and_section_order,
		type: "POST",
		dataType: "json",
		data: rewrite.manage.state.pages_and_sections_order_manifest(),
		mode: 'abort',
		success: rewrite.manage.handlers.save_section_and_page_response,
		error: rewrite.manage.handlers.response_error
     });
	rewrite.manage.ui.show_saving_pages_message();
}

rewrite.manage.ui.show_saving_pages_message = function() {
	$("status").html("Saving...");
}

rewrite.manage.ui.show_saved_pages_message = function() {
	$("status").html("Saved.");
}

////////////////////////////////////////////////////////////////////////
//////////////////////// EDITOR ////////////////////////////////////////
////////////////////////////////////////////////////////////////////////


rewrite.editor = {};
rewrite.editor.state = {};
rewrite.editor.urls = {};
rewrite.editor.handlers = {};
rewrite.editor.actions = {};
rewrite.editor.ui = {};

rewrite.editor.init = function() {
	rewrite.editor.state.init();
	rewrite.editor.urls.init();
	rewrite.editor.handlers.init();
	rewrite.editor.actions.init();
	rewrite.editor.ui.init();
}

rewrite.editor.state.init = function(){
	rewrite.editor.state.is_editing = false;
	rewrite.editor.state.node = $("#rewrite_editable_body");
	rewrite.editor.state.current_html = rewrite.editor.state.node.html();
};
rewrite.editor.urls.init = function(){};
rewrite.editor.handlers.init = function(){
	$(document).bind('keydown', 'ctrl+e', rewrite.editor.handlers.toggle_edit);
	$(document).bind('keydown', 'alt+e', rewrite.editor.handlers.toggle_edit);
	$(document).bind('keydown', 'meta+e', rewrite.editor.handlers.toggle_edit);
	$(document).bind('keydown', 'command+e', rewrite.editor.handlers.toggle_edit);

	$(document).bind('keydown', 'ctrl+s', rewrite.editor.handlers.save_page);
	$(document).bind('keydown', 'alt+s', rewrite.editor.handlers.save_page);
	$(document).bind('keydown', 'meta+s', rewrite.editor.handlers.save_page);
	$(document).bind('keydown', 'command+s', rewrite.editor.handlers.save_page);


	$(".edit_link").live('click', rewrite.editor.handlers.edit_link_clicked);
	$(".save_link").live('click', rewrite.editor.handlers.save_link_clicked);
	$(".cancel_link").live('click', rewrite.editor.handlers.cancel_link_clicked);
};
rewrite.editor.actions.init = function(){};
rewrite.editor.ui.init = function(){
	rewrite.editor.ui.update_mode_links();
};


rewrite.editor.state.get_page_html = function() {
	if (rewrite.editor.state.is_editing) {
		return nicEditors.findEditor('rewrite_editable_body').getContent();
	} else {
		return rewrite.editor.state.node.html();
	}
}

rewrite.editor.handlers.toggle_edit = function(){
	if (rewrite.editor.state.is_editing) {
		rewrite.editor.actions.turn_edit_mode_off();
	} else {
		rewrite.editor.actions.turn_edit_mode_on();
	}
	return false;
}
rewrite.editor.handlers.edit_link_clicked = function(){
	rewrite.editor.actions.turn_edit_mode_on();
	return false;
}

rewrite.editor.handlers.cancel_link_clicked = function(){
	rewrite.editor.actions.cancel_edit();	
	return false;
}

rewrite.editor.handlers.save_link_clicked = function(){
	rewrite.editor.actions.save_page();	
	return false;
}

rewrite.editor.actions.cancel_edit = function() {
	// Discard changes
	rewrite.editor.state.current_html = rewrite.editor.state.start_html;
	rewrite.editor.actions.turn_edit_mode_off();
}
rewrite.editor.actions.save_page = function() {
	$.ajax({
      url: rewrite.editor.urls.save_page,
      type: "POST",
      dataType: "json",
      data: {"content": rewrite.editor.state.get_page_html()},
      mode: 'abort',
      success: function(json) {
      	rewrite.editor.state.current_html = rewrite.editor.state.get_page_html();
      	rewrite.editor.actions.turn_edit_mode_off();
      },
      error: function() {
      	alert("error")
      }
 	});
}

rewrite.editor.actions.turn_edit_mode_on = function() {
	if (!rewrite.editor.state.is_editing) {
		rewrite.editor.state.start_html = rewrite.editor.state.node.html();
		rewrite.editor.state.editor = new nicEditor({fullPanel : true, iconsPath : STATIC_URL + 'images/rewrite/nicEditorIcons.gif'});
		rewrite.editor.state.editor.setPanel('rewrite_editor');
		rewrite.editor.state.editor.addInstance('rewrite_editable_body');
	}
	rewrite.editor.state.is_editing = true;
	rewrite.editor.ui.update_mode_links();
}
rewrite.editor.actions.turn_edit_mode_off = function() {
	if (rewrite.editor.state.is_editing) {
		rewrite.editor.state.start_html = "";
		rewrite.editor.state.editor.removeInstance('rewrite_editable_body');
		rewrite.editor.state.editor.removePanel();
		rewrite.editor.state.editor = null;
		$("#rewrite_admin_bar").append("<div id='rewrite_editor'></div>");
		rewrite.editor.state.node.html(rewrite.editor.state.current_html);
	}
	rewrite.editor.state.is_editing = false;
	rewrite.editor.ui.update_mode_links();

}

rewrite.editor.ui.update_mode_links = function() {
	if (rewrite.editor.state.is_editing) {
		$("#rewrite_admin_bar .edit_link").hide();
		$("#rewrite_admin_bar .save_links").show();
	} else {
		$("#rewrite_admin_bar .edit_link").show();
		$("#rewrite_admin_bar .save_links").hide();
	}
}