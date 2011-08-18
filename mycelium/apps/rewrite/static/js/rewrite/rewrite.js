var editor;
$(function(){
	var editing_nodes = [];
	
	var node = $("#rewrite_editable_body");
	$("#rewrite_admin_bar .edit_link").show();
	$("#rewrite_admin_bar .save_links").hide();

	$(".edit_link").live("click",function(){

		html = node.html();
		// node.html("<textarea name='temp_editing' id='panel1'>"+html+"</textarea>");
		// editor = new nicEditor({fullPanel : true}).panelInstance('panel1',{hasPanel : true});
		editor = new nicEditor({fullPanel : true, iconsPath : STATIC_URL + 'images/rewrite/nicEditorIcons.gif'});
		editor.setPanel('rewrite_editor');
        editor.addInstance('rewrite_editable_body');
		
		$("#rewrite_admin_bar .edit_link").hide();
		$("#rewrite_admin_bar .save_links").show();
		return false;
	});
	$(".save_link").live("click",function(){
		var new_html = nicEditors.findEditor('rewrite_editable_body').getContent();
		editor.removeInstance('rewrite_editable_body');
		editor.removePanel();
		$("#rewrite_admin_bar").append("<div id='rewrite_editor'></div>");
		editor = null;
		// var new_html = $("textarea[name=temp_editing]",node).val();
		node.html(new_html);

		// Save page
		$.ajax({
          url: urls.save_rewrite_page,
          type: "POST",
          dataType: "json",
          data: {"content":new_html},
          mode: 'abort',
          success: function(json) {
          	console.log("saved");
          },
          error: function() {
          	alert("error")
          }
     	});

		$("#rewrite_admin_bar .edit_link").show();
		$("#rewrite_admin_bar .save_links").hide();
		return false;
	});
	$(".cancel_link").live("click",function(){
		node.html(html);
		editor.removeInstance('rewrite_editable_body');
		editor.removePanel();
		$("#rewrite_admin_bar").append("<div id='rewrite_editor'></div>");
		editor = null;
		$("#rewrite_admin_bar .edit_link").show();
		$("#rewrite_admin_bar .save_links").hide();		
		return false;
	});
	$(".new_page_link").live("click", show_new_page_for_section);
	$(".cancel_new_page_link").live("click", hide_new_page_for_section);
	$(".new_section_link").live("click", show_new_section);
	$(".cancel_section_link").live("click", hide_new_section);
});

function editableNode(node) {
	this.real = true;
	this.node = $(node);
	this.html = this.node.html();
	$(node).html("<textarea name='temp_editing' id='"+edname(node)+"'>"+this.html+"</textarea>");
	new nicEditor({fullPanel : true}).panelInstance(edname(node),{hasPanel : true});
	this.editor = nicEditors.findEditor(edname(node));
	return this;
};
function edname(node) {
	return "editor_for_"+$(node).attr("id")
};

function show_new_page_for_section() {
	var section = $(this).parents("section");
	$(".new_page_form",section).show();
	$(".new_page_link",section).hide();
	return false;
}
function hide_new_page_for_section() {
	var section = $(this).parents("section");
	$(".new_page_form",section).hide();
	$(".new_page_link",section).show();
	return false;
}


function show_new_section() {
	$(".new_section_form").show();
	$(".new_section_link").hide();
	return false;
}
function hide_new_section() {
	$(".new_section_form").hide();
	$(".new_section_link").show();
	return false;
}