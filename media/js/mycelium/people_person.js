$(function(){
    $("#basic_info_form").bind("genericFieldForm.toggle_off", do_some_intelligent_data_formatting);
    $("#basic_info_form").bind("genericFieldForm.toggle_on", function(e){$(".city_state_comma",e.target).show();});
    $("#basic_info_form").genericFieldForm();
    $(".person_delete_btn").click(delete_person);
    intelligently_show_hide_comma();
    intelligently_show_no_home_contact_info();
    
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

    // End abstract this
});

function do_some_intelligent_data_formatting() {
    intelligently_show_hide_comma();
    intelligently_show_no_home_contact_info();
}

function intelligently_show_hide_comma() {
    var target = $("#basic_info_form");
    if ($("#container_id_city .view_field",target).html() != "" && $("#container_id_state .view_field").html() != "") {
        $(".city_state_comma",target).show();   
    } else {
        $(".city_state_comma",target).hide();
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

