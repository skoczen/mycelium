function bind_groups_tab_events() {
	$("tab_contents.people_groups_tab .groups_list").genericTags({'mode':'checkbox'});
	$("tab_contents.people_groups_tab .groups_list").bind("genericTags.bind_checkbox_inputs_if_needed", setup_columns);
	setup_columns();
}
function setup_columns() {
	$("tab_contents.people_groups_tab .groups_list tags fragment").columnize({ 'columns': 2 });	
}