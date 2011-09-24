$(function(){
	$(".help_btn").click(open_uservoice);
	$(".side_help_btn").click(toggle_help_popup);
	$(".close_help_popup_btn").click(close_help_popup);
	center_help_popup();
});

function open_uservoice() {
   UserVoice.showPopupWidget();
   close_help_popup();
}

function toggle_help_popup() {
	$("#help_popup").toggle();
	center_help_popup();
	$(".side_help_btn").toggleClass("current")
}
function center_help_popup() {
	var top_val = $(".side_help_btn").offset().top - $("#help_popup").outerHeight()/2;
	$("#help_popup").css("top",top_val)
}
function close_help_popup() {
   $("#help_popup").hide();
   $(".side_help_btn").removeClass("current")	
}

