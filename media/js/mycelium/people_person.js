$(function(){
	$(".striped tr:even").addClass("even");
	$(".striped tr:odd").addClass("odd");
	$(".save_info a").hide();

	$(".switch").click(toggle_edit);
	$("body").bind('keydown', 'ctrl+e', toggle_edit);
	$("body").bind('keydown', 'alt+e', toggle_edit);
	$("body").bind('keydown', 'meta+e', toggle_edit);
	$("body").bind('keydown', 'ctrl+f', focus_search);
	// $("input").check_width();
	$(".last_save_time").hide();
	$("form input").live("change", save_basic_form)
	$("form input").autoGrowInput({comfortZone: 30, resizeNow:true});

	$(".save_now_btn").live("click", save_basic_form)
	
	$("#id_page_top_search").bind("keydown", function(){
		setTimeout(function(){
			if ($("#id_page_top_search").val() == "") {
				$(".small_search .nyi").fadeOut();
			} else {
				$(".small_search .nyi").fadeIn();
			}
		}, 100)
	});
	{% if request.GET.edit == "ON" %}
	toggle_edit();
	{% endif %}
	intelligently_show_hide_comma();
});
function toggle_edit(){
	var box = $(".switch_box");
	if (box.hasClass("off")) {
		box.removeClass("off").addClass("on");
		$(".basic_info.view").hide();
		$(".basic_info.edit").show();
		$(".save_info a").show();
		$("#basic_info_form").removeClass("edit_mode_off").addClass("edit_mode_on");
		$(".last_save_time").fadeIn();
		$(".city_state_comma").show();
	} else {
		box.removeClass("on").addClass("off");
		$(".basic_info.view").show();
		$(".basic_info.edit").hide();
		$(".save_info a").hide();
		$("#basic_info_form").addClass("edit_mode_off").removeClass("edit_mode_on");
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
var saving_timeout;
function save_basic_form() {
	savingTimeout = setTimeout(function(){$(".last_save_time").html("Saving...");},200);
	$.ajax({
	  url: $("#basic_info_form").attr("action"),
	  type: "POST",
	  dataType: "json",
	  data: $.param( $("#basic_info_form input") ),
		  success: function(json) {
			clearTimeout(savingTimeout);
			$(".generic_editable_field").each(function(){
				var field = $(this);
				$(".view_field",field).html($(".edit_field input",field).val());
			});
			$(".last_save_time").hide();
			$(".last_save_time").html("Last saved a few seconds ago.").fadeIn();
		 },
	
		  error: function() {
			clearTimeout(savingTimeout);
			alert("error");
		  },
	});
}
