$(function(){
    $("#basic_info_form").bind("genericFieldForm.toggle_off", intelligently_show_hide_comma);
    $("#basic_info_form").bind("genericFieldForm.toggle_on", function(e){$(".city_state_comma",e.target).show();});
    $("#basic_info_form").genericFieldForm();
})

function intelligently_show_hide_comma(target) {
 if ($("#container_id_city .view_field",target).html() != "" && $("#container_id_state .view_field").html() != "") {
     $(".city_state_comma",target).show();   
 } else {
     $(".city_state_comma",target).hide();
 }
}
