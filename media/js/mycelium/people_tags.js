function bind_tags_tab_events() {
	$("tab_contents.people_tags_tab .tags_list").genericTags({'mode':'checkbox'});
	// $("#new_category").ajaxForm({"success":process_fragments_and_rebind_donation_form,"dataType": 'json'});
	$("tabbed_box[name=add_a_category]").bind("mycelium.tabbed_box.opened",function(){
        $("#new_category input[name$=name]").focus();
    });
	$("#new_category .cancel_add_btn").live("click", cancel_add_category);
}
function cancel_add_category() {
    $("tabbed_box[name=add_a_category] tab_title").trigger("click");
    return false;
}
