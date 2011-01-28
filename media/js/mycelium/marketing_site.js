$(function(){
    setupFooter();
    $(window).bind("resize",setupFooter);
});

function setupFooter(){
    footer = $("#footer");
    var footerHeight = footer.height()
    // console.log(footerHeight)
    // console.log($("HTML").height());
    // console.log($(window).height());
    
    if ($("html").height()+footerHeight < $(window).height()) {
        footer.css("position","fixed").css("bottom",0)
    } else {
        footer.css("position","relative")
    }

};