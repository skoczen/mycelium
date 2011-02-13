$(function(){
	$(".striped tr:even").addClass("even");
	$(".striped tr:odd").addClass("odd");
	$(".save_info a").hide();

	$(".switch").click(toggle_edit);
	$(".start_edit_btn").click(toggle_edit);
	$(".edit_done_btn").click(toggle_edit);
	$("body").bind('keydown', 'ctrl+e', toggle_edit);
	$("body").bind('keydown', 'alt+e', toggle_edit);
	$("body").bind('keydown', 'meta+e', toggle_edit);
	$("body").bind('keydown', 'ctrl+f', focus_search);
	// $("input").check_width();
	$(".last_save_time").hide();
	$("form input").live("change", queue_form_save);
	$("form input").live("keyup", queue_form_save);	
	$("form input").autoGrowInput({comfortZone: 30, resizeNow:true});

    // $(".save_and_status_btn").live("click", save_basic_form);
	
    console.log("register generic fields")
    
	$("#id_page_top_search").bind("keydown", function(){
		setTimeout(function(){
			if ($("#id_page_top_search").val() == "") {
				$(".small_search .nyi").fadeOut();
			} else {
				$(".small_search .nyi").fadeIn();
			}
		}, 100);
	});
	intelligently_show_hide_comma();
});
function toggle_edit(){

	if ($("#basic_info_form").hasClass("edit_mode_off")) {
        // box.removeClass("off").addClass("on");
		$("save_status_and_button .save_and_status_btn").show();
		$("save_status_and_button .start_edit_btn").hide();
		$("save_status_and_button .edit_done_btn").show();
		$(".basic_info.view").hide();
		$(".basic_info.edit").show();
		$(".save_info a").show();
		$("#basic_info_form").removeClass("edit_mode_off").addClass("edit_mode_on");
		$("#page").removeClass("edit_mode_off").addClass("edit_mode_on");
		$(".last_save_time").fadeIn();
		$(".city_state_comma").show();
	} else {
		$("save_status_and_button .save_and_status_btn").hide();
		$("save_status_and_button .start_edit_btn").show();
		$("save_status_and_button .edit_done_btn").hide();
        // box.removeClass("on").addClass("off");
		$(".basic_info.view").show();
		$(".basic_info.edit").hide();
		$(".save_info a").hide();
		$("#basic_info_form").addClass("edit_mode_off").removeClass("edit_mode_on");
		$("#page").addClass("edit_mode_off").removeClass("edit_mode_on");
		$(".last_save_time").fadeOut();		
		intelligently_show_hide_comma();
	}
	return false;
}
function focus_search(){
	$("#id_page_top_search").focus();
}
function intelligently_show_hide_comma() {
	if ($("#container_id_city .view_field").html() != "" && $("#container_id_state .view_field").html() != "") {
		$(".city_state_comma").show();	
	} else {
		$(".city_state_comma").hide();
	}
}

var form_save_timeout;
var MIN_SAVE_MESSAGE_DISPLAY_TIME = 1600;
function queue_form_save() {
    
    // if any fields have changed
    console.log("if any fields have changed")

    $(".save_and_status_btn").html("Save Now").addClass("mycelium_active_grey");
    clearTimeout(form_save_timeout)
    form_save_timeout = setTimeout(save_basic_form, 1000);
}

function save_basic_form() {
	$(".last_save_time").hide();	    
    $(".last_save_time").html("Saving changes...").fadeIn(50);
    var save_start_time = new Date();
	$.ajax({
	  url: $("#basic_info_form").attr("action"),
	  type: "POST",
	  dataType: "json",
	  data: $.param( $("#basic_info_form input") ),
		  success: function(json) {
			$(".generic_editable_field").each(function(){
				var field = $(this);
				$(".view_field",field).html($(".edit_field input",field).val());
			});
			var savetime = new Date();
			total_saving_time = savetime - save_start_time;
			console.log(total_saving_time)
			console.log(MIN_SAVE_MESSAGE_DISPLAY_TIME)
			if (total_saving_time < MIN_SAVE_MESSAGE_DISPLAY_TIME) {
			    setTimeout(show_saved_message,MIN_SAVE_MESSAGE_DISPLAY_TIME-total_saving_time);
			} else {
			    show_saved_message();
			}
		 },
	
		  error: function() {
			alert("error");
		  }
	});	
}
function show_saved_message(){
    $(".last_save_time").hide();
	$(".last_save_time").html("Saved a few seconds ago.").fadeIn();
	setTimeout(function(){
        $(".save_and_status_btn").html("Saved").removeClass("mycelium_active_grey");
	}, 200)
}