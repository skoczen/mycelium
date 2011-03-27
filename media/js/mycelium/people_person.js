$(function(){
    $(".person_delete_btn").click(delete_person);
    $("detail_tabs a.detail_tab").live("click",detail_tab_clicked);
    $(".general_person_tags").genericTags();
    default_tab = $.bbq.getState('current_detail_tab');
    if (default_tab !== undefined) {
        load_detail_tab(default_tab);
    }
});
var tag_fadeout_timeout = false;
var prev_tab_name = "#recent_activity";

function detail_tab_clicked(e) {
    var tab_link = $(e.target);
    var tab_name = tab_link.attr("href");
    load_detail_tab(tab_name);   
    return false;
}
function load_detail_tab(tab_name) {
    tab_link = $("detail_tabs a[href="+tab_name+"]");
    var tab_container = tab_link.parents("detail_tabs");
    if (tab_name != prev_tab_name) {
        // Switch the current tab
        prev_tab_name = tab_name;
        $("fragment[name=detail_tab]").html("Loading...");
        $(".detail_tab.current", tab_container).removeClass("current");
        tab_link.addClass("current");

        // Go get the tab content from the server.
        $.Mycelium.fragments.get_and_update_fragments(tab_container.attr("update_url"), {
            "data": {'tab_name': tab_name},
            "async": false
        });
        switch(tab_name){
            case "#volunteer":
                bind_volunteer_tab_events();
                break;
            case "#donor":
                bind_donor_tab_events();                
                break;
            case "#groups":
                bind_groups_tab_events();
                break;
            case "#tags":
            	bind_tags_tab_events();
            	break;
        }
        $.bbq.pushState({"current_detail_tab":tab_name})
    } 
}


function delete_person(e) {
    var name = $("#container_id_first_name .view_field").text() + " " + $("#container_id_last_name .view_field").text();
    if (name == " ") {
        name = "Unnamed Person";
    }
    if (confirm("Are you sure you want to completely delete " + name + " from the database? \n\nDeleting will remove this person, and all their data (contact info, job info, etc).  It cannot be undone.\n\nPress OK to delete "+ name +".\nPress Cancel to leave things unchanged.")) {
        $(window).unbind("unload.genericFieldForm");
        $("#delete_person_form").submit();
    }
}

