(function($){
    var methods = {
       init : function( options ) {
           var defaults = {
                "search_queue_delay_ms": 50, 
                "striped_results": true,
                "highlight_results": true,
                "focus_on_setup": true,
                "search_element": $("input[typeof=search]"),
                "results_element": $("search_results"),
                "search_url": "",
                "process_results_as_fragments": true,
                "process_results_as_replace_html": false,
                "bind_to_keydown": true,
                "bind_to_change": true,
                "results_processed_callback": function(){}
           };
                 
           var options =  $.extend(defaults, options);
 
           return this.each(function() {
                var $this = $(this),
                    data = $this.data('myceliumSearch');
                
                if (!data) {
                    data = {};
                    data.options = options;
                    data.target = $this;
                }

                data.queue_searching = function() {
                    clearTimeout(data.search_timeout);
                    data.search_timeout = setTimeout(data.update_search, data.options.search_queue_delay_ms);
                };
                data.format_search_response = function() {
                    if (data.options.highlight_results) {
                        $.Mycelium.highlight_search_terms(data.q,data.options.results_element);
                    }
                    if (data.options.striped_results) {
                        $.Mycelium.update_stripes(data.options.results_element);
                    }
                    data.options.results_processed_callback(data.options.search_element);                  
                };

                data.update_search = function() {
                    if (data.previous_query != $.trim(data.options.search_element.val())) {
                        data.q = $.trim(data.options.search_element.val());
                        data.previous_query = data.q;

                        $.ajax({
                          url: data.options.search_url,
                          type: "GET",
                          dataType: "json",
                          data: {'q':data.q},
                          mode: 'abort',
                          success: function(json) {
                            if (typeof(json) == typeof({})) {
                              if (data.options.process_results_as_fragments) {
                                  $.Mycelium.fragments.process_fragments_from_json(json);
                              }
                              if (data.options.process_results_as_replace_html) {
                                  $(data.options.results_element).html(json.html);
                              }                              
                              data.format_search_response();
                         }
                        }
                    });

                    }
                };

                data.previous_query = "%*(#:LKCL:DSF@()#SDF)";
                data.search_timeout = false;
                data.search_element = $(data.options.search_element);

                if (data.options.bind_to_keydown) {
                    data.search_element.live("keydown",data.queue_searching);            
                }
                if (data.options.bind_to_change) {
                    data.search_element.live("change",data.queue_searching);
                }
                data.search_element.bind('keyup', 'return', function(){
                    data.search_element.trigger("myceliumSearch.return_pressed");
                });

                if (data.options.focus_on_setup && !("autofocus" in document.createElement("input"))) {
                    data.search_element.focus();
                }
                
                qs = $.deparam.querystring();
                if (qs['q'] !== undefined) {
                  data.q = qs['q'];
                  data.previous_query = data.q;
                  data.search_element.val(data.q);
                  data.format_search_response();
                }


                $this.data('myceliumSearch',data);
            });
        }
    };


    $.fn.myceliumSearch = function( method ) {
       if ( methods[method] ) {
            return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));            
       } else if ( typeof method === 'object' || ! method ) {
         return methods.init.apply( this, arguments );
       } else {
         $.error( 'Method ' +  method + ' does not exist on jQuery.myceliumSearch' );
       }    
     };
     
})(jQuery);
