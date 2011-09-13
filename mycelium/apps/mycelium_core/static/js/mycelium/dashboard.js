$(function(){
	$(".yes_to_nickname").click(yes_to_nickname);	
	$(".no_to_nickname").click(no_to_nickname);
	$(".save_new_nickname").click(save_new_nickname);
	$("#id_new_nickname").bind('keydown', 'Enter' ,save_new_nickname);
	$("#id_new_nickname").bind('keydown', 'Return' ,save_new_nickname);
	$(".hide_challenge_complete_link").click(hide_challenge_complete);
	$(".older_news_link").click(show_older_news);
});

var nickname = false;
function yes_to_nickname(){
	nickname = $(".nickname_question .nickname_guess").html();
	update_with_new_nickname();
	return false;
}
function no_to_nickname(){
	$(".nickname_no_followup").show();
	$(".nickname_question .initial_question").hide();
	$("#id_new_nickname").focus();
	return false;
}
function save_new_nickname () {
	nickname = $("#id_new_nickname").val();
	update_with_new_nickname();
	return false;
}
function update_with_new_nickname(){
	$.ajax({
          url: $(".nickname_question").attr("save_url"),
          type: "POST",
          dataType: "json",
          data: {"nickname":nickname},
          mode: 'abort',
          success: function(json) {
			 $(".nickname_question").html("Got it. Thanks, "+nickname+"!");
          }
     });
}

function hide_challenge_complete(){
	link = $(this);
	$.ajax({
          url: link.attr("href"),
          type: "POST",
          dataType: "json",
          data: {},
          mode: 'abort',
          success: function(json) {
			 $(".challenge_complete_btn_area").html("Got it!");
			 setTimeout(function(){
			 	$(".challenges_complete_section").fadeOut();
			 },2000);
          }
     });
     return false;
}
function show_older_news() {
	$(".archived_news").removeClass("hidden").show();
	$(".older_news_link").hide();
}