$(function(){
	
})

function bind_groups_tab_events() {
    $(".people_groups_tab .group_tag_list").genericTags({'mode':'checkbox'});
$("tab_contents.people_groups_tab  .groups_list two_columns tags").columnize({ 'columns': 2 });
}