$(function(){
    $(".people_conversations_tab #new_conversation .cancel_add_btn").live("click", conversationTab.cancel_add_conversation);
    $(".people_conversations_tab .delete_conversation_btn").live("click",conversationTab.delete_conversation_from_people_tab);
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

conversationTab.cancel_add_conversation = function() {
    $("tabbed_box[name=add_a_conversation] tab_title").trigger("click");
    return false;
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
        // "gotoCurrent": true,
        "showCurrentAtPos": 1            
    });    
}

function process_fragments_and_rebind_conversation_form(json) {
        $.Mycelium.fragments.process_fragments_from_json(json);
        bind_conversation_tab_events();
}
