function setupFooter(){
    footer = $("#footer");
    var footerHeight = footer.height();
    if ($("html").height()+footerHeight < $(window).height()) {
        footer.css("position","fixed").css("bottom",0);
    } else {
        footer.css("position","relative");
    }
};
$(function(){
    setupFooter();
    $(window).bind("resize",setupFooter);
	$(window).resize(make_sure_home_boxes_are_equal_height);
	make_sure_home_boxes_are_equal_height();
});

function make_sure_home_boxes_are_equal_height() {
	var max_height = 50;
	$(".features .row").each(function() {
		row = $(this);
		$(".feature .description",row).css({"height": ""});

		$(".feature .description",row).each(function(){
			if ($(this).height()>max_height) {
				max_height = $(this).height();
			}
		})
		$(".feature .description",row).height(max_height);		

	});

}