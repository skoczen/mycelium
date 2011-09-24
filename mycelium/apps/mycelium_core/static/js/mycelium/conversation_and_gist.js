$(function(){
	$(".gist_and_remainder .see_all_link").live("click", show_conversation_remainder);
	$(".gist_and_remainder .hide_remainder_link").live("click", hide_conversation_remainder);
});

function show_conversation_remainder() {
	var con = $(this).parents(".gist_and_remainder");
	$(".see_all_link",con).hide();
	$(".remainder", con).show();
	$(".hide_remainder_link",con).show().css("display","block");
	return false;
}

function hide_conversation_remainder() {
	var con = $(this).parents(".gist_and_remainder");
	$(".see_all_link",con).show();
	$(".remainder", con).hide();
	$(".hide_remainder_link",con).hide();
	return false;
}
