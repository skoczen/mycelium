$(function(){
  var tabs = $('.tabs'),
  tab_a_selector = 'ul.ui-tabs-nav a';
  tabs.tabs({ event: 'change' });
  
  tabs.find( tab_a_selector ).click(function(){
	  var state = {},
      
      id = $(this).closest( '.tabs' ).attr( 'id' ),
      url = $(this).attr( 'href' ).replace( /^#/, '' );
      state[ id ] = url;
      $.bbq.pushState( state );
      return false;
  });
  
  $(window).bind( 'hashchange', function(e) {
    tabs.each(function(){
      var idx = $.bbq.getState( this.id, true ) || 0;
      $(this).find( tab_a_selector + "[href^=#"+idx+"]").triggerHandler( 'change' );
    });
  })
  $(window).trigger( 'hashchange' );

});