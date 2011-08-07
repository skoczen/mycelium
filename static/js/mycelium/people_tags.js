function bind_tags_tab_events() {
	$("tab_contents.people_tags_tab .tags_list").genericTags({'mode':'checkbox'});
}

function process_fragments_and_rebind_tags_form(json) {
    $.Mycelium.fragments.process_fragments_from_json(json);
    bind_tags_tab_events();
}
