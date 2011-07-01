$(function(){
    $("#basic_info_form").bind("genericFieldForm.toggle_off", do_some_intelligent_data_formatting);
    $("#basic_info_form").bind("genericFieldForm.toggle_on", function(e){$(".city_state_comma",e.target).show();$(".birthday").show();});
    $("#basic_info_form").genericFieldForm();
    intelligently_show_hide_comma();
    intelligently_show_no_home_contact_info();
});

function do_some_intelligent_data_formatting() {
    intelligently_show_hide_comma();
    intelligently_show_no_home_contact_info();
}

function intelligently_show_hide_comma() {
    var target = $("#basic_info_form");
    // city state
    if ($("#container_id_city .view_field",target).html() != "" && $("#container_id_state .view_field").html() != "") {
        $(".city_state_comma",target).show();   
    } else {
        $(".city_state_comma",target).hide();
    }
    // birthday
    if ($("#container_id_birth_month .view_field",target).html() != "" && $("#container_id_birth_year .view_field").html() != "") {
        $(".date_year_comma",target).show();
    } else {
        $(".date_year_comma",target).hide();
    }
    if ($("#container_id_birth_month .view_field",target).html() != "" || $("#container_id_birth_year .view_field").html() != "" || $("#container_id_birth_date .view_field").html() != "" ) {
		$(".birthday").show();
    } else {
    	$(".birthday").hide();
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
