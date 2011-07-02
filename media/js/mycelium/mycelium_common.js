$(function(){
	$(".help_btn").click(open_uservoice);
});

function open_uservoice() {
   UserVoice.showPopupWidget();
}