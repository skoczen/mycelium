var scroll_options = {
    duration:400, 
    margin: true,
    offset: 0
};

$(function(){
    $("#id_search_new_person").myceliumSearch({
        search_element: $("#id_search_new_person"),
        search_url: $("#id_search_new_person").attr("results_url"),
        results_element: $("fragment[name=new_person_search_results]")
    });    
    $("tabbed_box[name=add_a_person] tab_title").live("click",start_add_new_person_to_org).bind("mycelium.tabbed_box.opened",open_tabbed_box).bind("mycelium.tabbed_box.closed",close_tabbed_box);;
    $(".not_in_goodcloud_btn").live("click",show_new_person_add_form);
    $(".select_person_to_add_btn").live("click",show_existing_person_add_form);
    $(".cancel_add_btn").live("click",cancel_add_person);
    $("#up_to_search").live("click",up_to_search_clicked);

	$("pane.pane_2 input").autoGrowInput({comfortZone: 30, resizeNow:true});    
    $("employee").genericFieldForm();
    $(".delete_contact_btn").live("click", confirm_employee_removal);
    $(".org_delete_btn").live("click",delete_organization);

    $(".general_organization_tags").genericTags();        
});

function start_add_new_person_to_org() {
    $(".add_new_person_btn").hide();
    $("tabbed_box box_content").height("auto");
    $("#search_for_person").show();
    $("#id_search_new_person").focus();
    return false;
}
function show_existing_person_add_form() {
    btn = $(this);
    row = btn.parents(".person_row");
    $("#add_existing_person").show();
    $("#add_existing_person .full_name").html($(".name",row).text());
    $("#add_existing_person input[name=person_pk]").val(row.attr("person_pk"));
    $("#new_person").hide();
    scroll_to_pane_2();
    $("#add_existing_person input[name$=role]").focus();
    return false;
}
function show_new_person_add_form() {
    $("#add_existing_person").hide();
    $("#new_person").show();
    var possible_names = $("#id_search_new_person").val().split(" ");
    if (possible_names.length > 0) {
        $("#new_person input[name$=first_name]").val(possible_names[0]);
    } 
    if (possible_names.length > 1) {
        $("#new_person input[name$=last_name]").val(possible_names[1]);
    }
    scroll_to_pane_2();
    $("#new_person input[name$=first_name]").focus();
    return false;
}
function cancel_add_person(){
    $("tabbed_box[name=add_a_person] tab_title").trigger("click");
    close_tabbed_box();
    $("pane[name=2]").hide();
    return false;
}
function up_to_search_clicked(){
    scroll_to_pane_1();
    return false;
}
function scroll_to_pane_1() {
    var my_options = {
        onAfter: function(){
            $("pane[name=2]").hide();
            $("tabbed_box box_content").height("auto");
        }
    };
	$.extend(true, my_options, scroll_options);
    
    $("tabbed_box box_content").height($("pane[name=1]").height());
    $("tabbed_box box_content").scrollTo("pane[name=1]", my_options);
}
function scroll_to_pane_2() {
    var my_options = {
        
    };
	$.extend(true, my_options, scroll_options);
	    
    $("pane[name=2]").show();    
    $("tabbed_box box_content").height($("pane[name=2]").height()-10);
    $("tabbed_box box_content").scrollTo("pane[name=2]", my_options);
}
function open_tabbed_box(){
    
}
function close_tabbed_box(){
    scroll_to_pane_1();
    $("#id_search_new_person").val("");
    $("fragment[name=new_person_search_results]").html("");
    $("pane[name=2]").hide();
}
function confirm_employee_removal(e) {
    var t = $(e.target);
    var emp = t.parents("employee");
    var name = $(".name",emp).text();
    var org_name = $(".basic_info .name_phone_email .name .view_field").text();
    emp.addClass("warning");
    var do_it = confirm("Are you sure you want to remove "+name+" from "+org_name+"?\n\nThis will not remove "+name+" from the database, only from this role at "+org_name+".");
    if (!do_it) {
        emp.removeClass("warning");
    }
    return do_it;
}
function delete_organization(e) {
    var name = $("#container_id_name .view_field").text();
    if (name == "") {
        name = "Unnamed Organization";
    }
    if (confirm("Are you sure you want to completely delete " + name + " from the database? \n\nDeleting will remove this organization and all their data (contact info, employees, etc).  The people associated with this organization will not be removed.\n\nThis action cannot be undone.\n\nPress OK to delete "+ name +".\nPress Cancel to leave things unchanged.")) {
        $(window).unbind("unload.genericFieldForm");
        $("#delete_org_form").submit();
    }
}