$(function(){
    $(".person_delete_btn").click(delete_person);
    $("detail_tabs a.detail_tab").live("click",detail_tab_clicked);
    
    
    // TODO: abstract this
	$(".new_tag input[name=new_tag]").autoGrowInput({comfortZone: 20, resizeNow:true});
    $(".new_tag input[name=new_tag]").live("keyup",function(e){
        if ($(e.target).val() != "") {
            $(".tag_add_btn",$(e.target).parents(".new_tag")).show();
        } else {
            $(".tag_add_btn",$(e.target).parents(".new_tag")).hide();
        }
    });
    $("#new_tag_form").ajaxForm({
        success: function(json){
            $.Mycelium.fragments.process_fragments_from_json(json);
            $(".new_tag input[name=new_tag]").val("");
            set_tag_results_fadeout($(".new_tag_list"),0)
        },
        dataType: 'json'
    });
    $("tag .remove_tag_link").live("click", function(){
       $.ajax({
         url: $(this).attr("href"),
         type: "GET",
         dataType: "json",
         success: function(json) {
            $.Mycelium.fragments.process_fragments_from_json(json);
         },
       });
       return false;
    });
    $.Mycelium.search.setUp({
        search_element: $(".new_tag input[name=new_tag]"),
	    search_url: $(".new_tag input[name=new_tag]").attr("results_url"),
	    results_element: $("fragment[name=new_tag_search_results]"),
	    striped_results: false,
	    results_processed_callback: new_tag_results,
        // bind_to_change: false,
    });
    $("tags a.tag_suggestion_link").live("click",function(){
        clear_tag_results_fadeout();
        $(".new_tag input[name=new_tag]",$(this).parents("tags")).val($(this).text());
        set_tag_results_fadeout($(".new_tag_list",$(this).parents("tags")), 10);
        return false;
    });
	$(".new_tag input[name=new_tag]").live("focus",function(){
        clear_tag_results_fadeout();
	    if ($(this).val() != "") {
            new_tag_results();
	    }
	});
	$(".new_tag input[name=new_tag]").live("blur",function(){
        set_tag_results_fadeout($(".new_tag_list",$(this).parents("tags")))
	});
    move_tag_results();
    // End abstract this
});
var tag_fadeout_timeout = false;

function detail_tab_clicked(e) {
    tab_link = $(e.target);
    tab_container = tab_link.parents("detail_tabs")
    // Switch the current tab
    $("fragment[name=detail_tab]").html("Loading...");
    $(".detail_tab", tab_container).removeClass("current");
    tab_link.addClass("current");
    
    // Go get the tab content from the server.
    $.Mycelium.fragments.get_and_update_fragments(tab_container.attr("update_url"), {
        "data": {'tab_name': tab_link.attr("href")}
    });


    return false;
}

function set_tag_results_fadeout(t, timeout) {
    if (timeout === undefined) {
        timeout = 500;
    }
    tag_fadeout_timeout = setTimeout(function(){
        t.hide();
        t.parents("search_results").removeClass("visible");
    }, timeout);
    
}
function clear_tag_results_fadeout() {
    clearTimeout(tag_fadeout_timeout);
}
function new_tag_results(ele){
    move_tag_results();
    var list = $("tags search_results");
    if (!list.hasClass("visible")) {
        list.addClass("visible");
        $(".new_tag_list",list).fadeIn();
    } else {
        $(".new_tag_list",list).show();
    }
}
function move_tag_results() {
    if ($("tags input[name=new_tag]").length) {
        var o = $("tags input[name=new_tag]").offset();
        $("tags search_results").offset({"top":o.top+10, "left":o.left});
    }
}


function intelligently_show_no_home_contact_info() {
    var some_contact_info = false;
    $("#basic_info_form tabbed_box[name=home] input").each(function(){
        if ($(this).val() != "") {
            some_contact_info = true;
        }
    });
    if (!some_contact_info) {
        $("#no_home_contact_info_message").html("No home contact information.");
    } else {
        $("#no_home_contact_info_message").html("");
    }
}

function delete_person(e) {
    var name = $("#container_id_first_name .view_field").text() + " " + $("#container_id_last_name .view_field").text();
    if (name == " ") {
        name = "Unnamed Person";
    }
    if (confirm("Are you sure you want to completely delete " + name + " from the database? \n\nDeleting will remove this person, and all their data (contact info, job info, etc).  It cannot be undone.\n\nPress OK to delete "+ name +".\nPress Cancel to leave things unchanged.")) {
        $("#delete_person_form").submit();
    }
}

