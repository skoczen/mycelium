function bind_tags_tab_events() {
	$("tab_contents.people_tags_tab .tags_list").genericTags({'mode':'checkbox'});
	// $("tab_contents.people_tags_tab .tags_list").bind("genericTags.bind_checkbox_inputs_if_needed", setup_columns);
	// setup_columns();
}
// function setup_columns() {
// 	$("tab_contents.people_tags_tab .tags_list tags fragment").columnize({ 'columns': 2 });	
// }