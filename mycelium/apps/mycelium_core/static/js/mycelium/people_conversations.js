$(function(){
    $(".people_conversations_tab #new_conversation .cancel_add_btn").live("click", conversationTab.cancel_add_conversation);
    $(".people_conversations_tab .delete_conversation_btn").live("click",conversationTab.delete_conversation_from_people_tab);
    $(".read_all_link").live("click",conversationTab.show_full_conversation_text);
    $(".read_less_link").live("click",conversationTab.hide_full_conversation_text);
    $(".more_conversations_link").live("click",conversationTab.show_more_conversations);
    $("#new_conversation .conversation_type label").live("click",conversationTab.conversation_type_label_clicked);
    $("#new_conversation #id_body").autoGrow();
	bind_conversation_tab_events();
});


var conversationTab = new Object();

conversationTab.delete_conversation_from_people_tab = function() {
	var row = $(this).parents(".conversation_row");
	row.addClass("pre_delete");
	var confirm_response = confirm("Are you sure you want to remove this conversation?\n\nPress OK to remove the conversation.\nPress Cancel to leave things as-is.");
	if (confirm_response) {
		$.ajax({
			url: $(this).attr("href"),
			type: "GET",
			dataType: "json",
			success: function(json) {
			$.Mycelium.fragments.process_fragments_from_json(json);
            process_fragments_and_rebind_conversation_form(json);
			}
		});		
	} else {
		row.removeClass("pre_delete");		
	}
	
    return false;	
}

conversationTab.cancel_add_conversation = function () {
    $("tabbed_box[name=add_a_conversation] tab_title").trigger("click");
    return false;
}

conversationTab.show_full_conversation_text = function () {
	var parent = $(this).parents(".conversation_body");
	$(".full_body",parent).removeClass("hidden").show();
	$(".gist",parent).hide();
	$(".read_all_link",parent).hide();
	return false
}
conversationTab.hide_full_conversation_text = function () {
	var parent = $(this).parents(".conversation_body");
	$(".full_body",parent).hide();
	$(".gist",parent).show();
	$(".read_all_link",parent).show();
	return false
}
conversationTab.show_more_conversations = function () {
	$(".showing_conversations").html($(".showing_conversations").html()+$("fragment[name=more_conversations] .conversation_list").html());
	$("fragment[name=more_conversations]").html("Loading...");
	$.ajax({
		url: $(this).attr("href"),
		type: "GET",
		dataType: "json",
		success: function(json) {
			$.Mycelium.fragments.process_fragments_from_json(json);
			$.Mycelium.update_stripes();
		}
	});	
	return false;
}
conversationTab.conversation_type_label_clicked = function () {
	$("#new_conversation .conversation_type label").removeClass("selected");
	$(this).addClass("selected");
}


function bind_conversation_tab_events() {
    $("#new_conversation").ajaxForm({
        "success":process_fragments_and_rebind_conversation_form,
        "dataType": 'json'
    });
    $("tabbed_box[name=add_a_conversation]").bind("mycelium.tabbed_box.opened",function(){
        $("#new_conversation textarea[name$=body]").focus();
    });
    
    $("#new_conversation input[name=date]").datepicker({
        "numberOfMonths": 2,
        "showButtonPanel": true,
        "gotoCurrent": true,
        "showCurrentAtPos": 1            
    });
    $.Mycelium.update_stripes();

    // $(".datepicker").datepicker({ dateFormat: 'yy-mm-dd-yy' });
}

function process_fragments_and_rebind_conversation_form(json) {
        $.Mycelium.fragments.process_fragments_from_json(json);
        bind_conversation_tab_events();
        $.Mycelium.update_stripes();
}
