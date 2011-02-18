$(function(){
    $.Mycelium.search.setUp({
        search_element: $("#id_search_new_person"),
	    search_url: $("#id_search_new_person").attr("results_url"),
	    results_element: $("fragment[name=new_person_search_results]")
    });
    $(".add_new_person_btn").live("click",start_add_new_person_to_org);
    $(".not_in_goodcloud_btn").live("click",show_new_person_add_form);
    $(".select_person_to_add_btn").live("click",show_existing_person_add_form);
    $(".cancel_add_btn").live("click",cancel_add_person);
});

function start_add_new_person_to_org() {
    $(".add_new_person_btn").hide();
    $(".add_person_container").show();
    $("#search_for_person").show();

}
function show_existing_person_add_form() {
    btn = $(this);
    row = btn.parents(".person_row");
    $("#add_existing_person").show();
    $("#add_existing_person .full_name").html($(".name",row).text());
    $("#add_existing_person input[name=person_pk]").val(row.attr("person_pk"));    
    $("#new_person").hide();
}
function show_new_person_add_form() {
    $("#add_existing_person").hide();
    $("#new_person").show();
}
function cancel_add_person(){
    $(".add_new_person_btn").show();
    $(".add_person_container").hide();
    $("#search_for_person").hide();
    $("#add_existing_person").hide();
    $("#new_person").hide();

}