$(function(){
	
	// $(".tab_content").hide()
	// var biggest_content = 0;
	// $(".tab_content").each(function(){
	// 	if ($(this).height() > biggest_content) {
	// 		biggest_content = $(this).height()
	// 	}
	// })
	// $("#side_nav ul").height(biggest_content+20);
});
$(function(){
  var tabs = $('.tabs'),
  tab_a_selector = 'ul.ui-tabs-nav a';
  tabs.tabs({ event: 'change' });
  
  tabs.find( tab_a_selector ).click(function(){
	  var state = {},
      
      id = $(this).closest( '.tabs' ).attr( 'id' ),
      idx = $(this).parent().prevAll().length;
    
      state[ id ] = idx;
      $.bbq.pushState( state );
  });
  
  $(window).bind( 'hashchange', function(e) {
    tabs.each(function(){
      var idx = $.bbq.getState( this.id, true ) || 0;
      $(this).find( tab_a_selector ).eq( idx ).triggerHandler( 'change' );
    });
  })
  $(window).trigger( 'hashchange' );

  setupFooter();
});