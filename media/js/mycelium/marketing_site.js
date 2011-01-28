$(function(){
    setupFooter();
    $(window).bind("resize",setupFooter);
});

function setupFooter(){
    footer = $("#footer");
    var footerHeight = footer.height()
    if ($(document).height()+footerHeight < $(window).height()) {
        footer.css("position","fixed").css("bottom",0)
    } else {
        footer.css("position","relative")
    }

};