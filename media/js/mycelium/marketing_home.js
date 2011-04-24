$(function(){
	$(window).resize(make_sure_home_boxes_are_equal_height);
	make_sure_home_boxes_are_equal_height();
});

function make_sure_home_boxes_are_equal_height() {
	var max_height = 50;
	$(".home_box .description").css({"height": ""});

	$(".home_box .description").each(function(){
		if ($(this).height()>max_height) {
			max_height = $(this).height();
		}
	})
	$(".home_box .description").height(max_height);
}