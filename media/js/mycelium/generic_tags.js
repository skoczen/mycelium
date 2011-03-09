    
// Generic tags
(function($){
    var methods = {
       init : function( options ) {
           var defaults = {
               "autogrow_tag_name": true,
               "autogrow_options": {comfortZone: 20, resizeNow:true},
               "form_selector": ".new_tag_form",
               "default_fade_timeout": 500
           }
                 
           var options =  $.extend(defaults, options);
 
           return this.each(function() {
                var $this = $(this),
                    data = $this.data('genericTags');
                
                
                if (!data) {
                    data = {};
                    data.options = options
                    data.target = $this;
                }

                data.new_input_field = $(".new_tag input[name=new_tag]", data.target)
                
                if (data.options.autogrow_tag_name) {
                    data.new_input_field.autoGrowInput(data.options.autogrow_options);                    
                }
                    
                data.new_input_field.bind("keyup",function(e){
                    if ($(e.target).val() != "") {
                        $(".tag_add_btn",$(e.target).parents(".new_tag")).show();
                    } else {
                        $(".tag_add_btn",$(e.target).parents(".new_tag")).hide();
                    }
                });

                data.new_tag_results = function(){
                    if (data){
                        data.move_tag_results();
                        var list = $("tags search_results", data.target);
                        if (!list.hasClass("visible")) {
                            list.addClass("visible");
                            $(".new_tag_list",list).fadeIn();
                        } else {
                            $(".new_tag_list",list).show();
                        }                
                    }        
                }
                data.move_tag_results = function() {
                    if (data){
                        console.log(data.new_input_field.length)
                        if (data.new_input_field.length) {
                            var o = data.new_input_field.offset();
                            console.log(o)
                            $("tags search_results",data.target).offset({"top":o.top+10, "left":o.left});
                        }                
                    } else {
                    }
                    
                }
                data.set_tag_results_fadeout = function (t, timeout) {
                    if (timeout === undefined) {
                        timeout = data.options.default_fade_timeout;
                    }
                    data.tag_fadeout_timeout = setTimeout(function(){
                        t.hide();
                        t.parents("search_results").removeClass("visible");
                    }, timeout);
                }

                data.clear_tag_results_fadeout = function() {
                    clearTimeout(data.tag_fadeout_timeout);
                }
                $(data.options.form_selector, data.target).ajaxForm({
                    success: function(json){
                        $.Mycelium.fragments.process_fragments_from_json(json);
                        data.new_input_field.val("");
                        data.set_tag_results_fadeout($(".new_tag_list", data.target),0);
                    },
                    dataType: 'json'
                });
                $("tag .remove_tag_link", data.target).live("click", function(){
                   $.ajax({
                     url: $(this).attr("href"),
                     type: "GET",
                     dataType: "json",
                     success: function(json) {
                        $.Mycelium.fragments.process_fragments_from_json(json);
                     },
                   });
                   return false;
                });
                $.Mycelium.search.setUp({
                    search_element: data.new_input_field,
                    search_url: data.new_input_field.attr("results_url"),
                    results_element: $("fragment[name=new_tag_search_results]", data.target),
                    striped_results: false,
                    results_processed_callback: data.new_tag_results,
                });
                $("tags a.tag_suggestion_link", data.target).live("click",function(){
                    data.clear_tag_results_fadeout();
                    data.new_input_field.val($(this).text());
                    data.set_tag_results_fadeout($(".new_tag_list", data.target),10);
                    return false;
                });
                data.new_input_field.bind("focus",function(){
                    data.clear_tag_results_fadeout();
                    if ($(this).val() != "") {
                        data.target.genericTags('new_tag_results');
                    }
                });
                data.new_input_field.bind("blur",function(){
                    data.set_tag_results_fadeout($(".new_tag_list", data.target));
                });
                data.move_tag_results(data.target);

                $this.data('genericTags',data)
            });
        },
       

    };


    $.fn.genericTags = function( method, do_not_call ) {
       if ( methods[method] ) {
        if (do_not_call !== true) {
            return methods[method]
        } else {
            return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));            
        }
       } else if ( typeof method === 'object' || ! method ) {
         return methods.init.apply( this, arguments );
       } else {
         $.error( 'Method ' +  method + ' does not exist on jQuery.genericTags' );
       }    
     };
     
})(jQuery);
