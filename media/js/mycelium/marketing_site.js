(function($){
    setupFooter();
    $(window).bind("resize",setupFooter);
	$(window).resize(make_sure_identical_height_block_boxes_are_equal_height);
	make_sure_identical_height_block_boxes_are_equal_height();
	$(".contact_button.online").click(open_uservoice);
	$.preloadCssImages();

});

function setupFooter(){
	if (!$.browser.msie) {
	    var footer = $("#footer");
	    var footerHeight = footer.height()+20;
	    if ($(document.body).height()+footerHeight < $(window).height()) {
	        footer.css("position","fixed").css("bottom",0);
	    } else {
	        footer.css("position","relative");
	    }
	}
};

function make_sure_identical_height_block_boxes_are_equal_height() {
	var max_height = 50;
	$(".row").each(function() {
		row = $(this);
		$(".identical_height_block",row).css({"height": ""});

		$(".identical_height_block",row).each(function(){
			if ($(this).height()>max_height) {
				max_height = $(this).height();
			}
		})
		$(".identical_height_block",row).height(max_height);		

	});

}
function open_uservoice() {
	UserVoice.showPopupWidget();
}