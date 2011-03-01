$(function(){
// Set up Mycelium object
	if ($.Mycelium === undefined) {
		$.Mycelium = new Object();
	}
	if (typeof(SEARCH_URL) == "undefined") {
	    var SEARCH_URL = ""
	}

// Fragments handler
	var fragments = new Object();
	
	fragments.options = {
	    json_dict_name: "fragments"
	};
	
    fragments.process_fragments_from_json = function(json) {
        if (json[fragments.options.json_dict_name] != undefined) {
            return fragments.process_fragments(json[fragments.options.json_dict_name]);
        } else {
            return fragments.process_fragments(json);
        }
    }
    
	fragments.process_fragments = function(fragment_dict) {
	    $("fragment").each(function(){
	        frag = $(this);
	        if (fragment_dict.hasOwnProperty(frag.attr("name"))) {
	           frag.trigger("fragments."+frag.attr("action"), fragment_dict[frag.attr("name")]);
	        }
	    });
	    return true;
	};
	
	fragments.replace_content = function(e, new_content) {
        $(e.target).html(new_content);
	};
	fragments.append_content = function(e, new_content) {
	    $(e.target).append(new_content);
	};
	fragments.clear_content = function(e, new_content) {
        $(e.target).html("");
	};
    // Default fragment actions:
    // replace
    // append
    // clear
	$("fragment").bind("fragments.replace",fragments.replace_content);
	$("fragment").bind("fragments.append",fragments.append_content);
	$("fragment").bind("fragments.clear",fragments.clear_content);

	$.Mycelium.fragments = fragments;


// Search handler
	var sh = new Object();
	
	sh.options = {
	    search_queue_delay_ms: 50, 
	    striped_results: true,
	    highlight_results: true,
	    focus_on_setup: true,
	    search_element: $("input[type=search]"),
	    results_element: $("search_results"),
	    search_url: SEARCH_URL,
	    process_results_as_fragments: true,
	    process_results_as_replace_html: false,
	    bind_to_keydown: true,
	    bind_to_change: true,
	    results_processed_callback: function(){},
	}
	sh.previous_query = "%*(#:LKCL:DSF@()#SDF)";
    sh.search_timeout = false;

	sh.setUp = function (options) {
		$.extend(true, sh.options, options);
        var t = $(sh.options.search_element);
        if (sh.options.bind_to_keydown) {
            t.live("keydown",sh.queue_searching);            
        }
        if (sh.options.bind_to_change) {
            t.live("change",sh.queue_searching);
        }
        t.bind('keyup', 'return', function(){
            t.trigger("mycelium.search.return_pressed");
        });

        if (sh.options.focus_on_setup && !("autofocus" in document.createElement("input"))) {
            t.focus();
        }
	}
	
    sh.queue_searching = function() {
    	clearTimeout(sh.search_timeout);
    	sh.search_timeout = setTimeout(sh.update_search, sh.options.search_queue_delay_ms);
    }

    sh.update_search = function() {
        if (sh.previous_query != $.trim(sh.options.search_element.val())) {
            sh.q = $.trim(sh.options.search_element.val());
            sh.previous_query = sh.q;

            $.ajax({
              url: sh.options.search_url,
              type: "GET",
              dataType: "json",
              data: {'q':sh.q},
              mode: 'abort',
              success: function(json) {
                if (typeof(json) == typeof({})) {
                    if (sh.options.process_results_as_fragments) {
                        $.Mycelium.fragments.process_fragments_from_json(json)
                    }
                    if (sh.options.process_results_as_replace_html) {
                        $(sh.options.results_element).html(json.html);
                    }
                    if (sh.options.highlight_results) {
                        $.Mycelium.highlight_search_terms(sh.q,sh.options.results_element);
                    }
                    if (sh.options.striped_results) {
                        $.Mycelium.update_stripes(sh.options.results_element);
                    }
                    sh.options.results_processed_callback(sh.options.search_element);
                }
        	 },
        	});

        }
    }
	$.Mycelium.search = sh;
	
	
// Generic Fields
(function($){
    var methods = {
       init : function( options ) {
           var defaults = {
               "min_save_message_display_time": 1600,
               "start_edit_btn_class": "save_status_and_button .start_edit_btn",
               "done_edit_btn_class": "save_status_and_button .edit_done_btn",
               "save_and_status_btn_class": "save_status_and_button .save_and_status_btn",
               "last_save_time_class": ".last_save_time",
               "save_now_text": "Save Now",
               "save_now_class": "mycelium_active_grey",
               "saved_text": "Saved",
               "saved_class": "mycelium_grey",
               "saving_text": "Saving",
               "saving_class": "mycelium_grey",
               "last_saved_saving_text": "Saving changes...",               
               "saved_recently_text": "Saved a few seconds ago.",
           }
                 
           var options =  $.extend(defaults, options);
 
           return this.each(function() {
                var $this = $(this),
                    data = $this.data('genericFieldForm');
                
                
                if (!data) {
                    data = {};
                    data.options = options
                    data.target = $this;
                    if (options.hasOwnProperty("form")) {
                        data.form = $(options.form)
                    } else {
                        if (data.target.is("form")) {
                            data.form = data.target;
                        } else {
                            if ($("form",data.target).length > 0) {
                                data.form = $("form:nth(0)",data.target);
                            } else {
                                data.form = data.target.parents("form");
                            }
                        }
                    }
                    data.save_url = (options.hasOwnProperty("save_url"))? options.save_url: data.form.attr("action");
                    data.save_method = (options.hasOwnProperty("save_method"))? options.save_method: data.form.attr("method");
                    data.async = true;
                    $this.data('genericFieldForm',data)
                    data = $this.data('genericFieldForm');
                }

                data.form_save_timeout = null;
                data.previous_serialized_str = "";
                
                $(data.options.start_edit_btn_class,data.target).click(function(){data.target.genericFieldForm('toggle_edit')});
                $(data.options.done_edit_btn_class,data.target).click(function(){data.target.genericFieldForm('toggle_edit')});

                $("body").bind('keydown', 'ctrl+e',  function(){data.target.genericFieldForm('toggle_edit')});
                $("body").bind('keydown', 'alt+e',   function(){data.target.genericFieldForm('toggle_edit')});
                $("body").bind('keydown', 'meta+e',  function(){data.target.genericFieldForm('toggle_edit')});
                $("body").bind('keydown', 'meta+s',  function(){data.target.genericFieldForm('save_and_status_btn_clicked')});
                $("body").bind('keydown', 'ctrl+s',  function(){data.target.genericFieldForm('save_and_status_btn_clicked')});
                $("input").bind('keydown', 'meta+s', function(){data.target.genericFieldForm('save_and_status_btn_clicked')});
                $("input").bind('keydown', 'ctrl+s', function(){data.target.genericFieldForm('save_and_status_btn_clicked')});

                $(data.options.last_save_time_class,data.target).hide();
                $("input", data.target).live("change", function(){data.target.genericFieldForm('queue_form_save')});
                $("input", data.target).live("keyup",  function(){data.target.genericFieldForm('queue_form_save')});
                $("input", data.target).autoGrowInput({comfortZone: 30, resizeNow:true});

                $(data.options.save_and_status_btn_class, data.target).live("click", function(){data.target.genericFieldForm('save_and_status_btn_clicked')});

                data.previous_serialized_str = data.form.serialize();
                $this.data('genericFieldForm',data)
                
                // bind to window close, confirm if there's anything in the ajax queue
                $(window).unload(function(){
                    data.async = false;
                    data.target.genericFieldForm('save_form');
                });
            });
        },
        
        toggle_edit: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericFieldForm');
                
            	if (data.target.hasClass("edit_mode_off")) {
            		$(data.options.save_and_status_btn_class,data.target).show();
            		$(data.options.start_edit_btn_class,data.target).hide();
            		$(data.options.done_edit_btn_class,data.target).show();

                    data.target.removeClass("edit_mode_off").addClass("edit_mode_on");
            		$(data.options.last_save_time_class,data.target).fadeIn();
            		data.target.trigger("genericFieldForm.toggle_on");
            	} else {
            		$(data.options.save_and_status_btn_class,data.target).hide();
            		$(data.options.start_edit_btn_class,data.target).show();
            		$(data.options.done_edit_btn_class,data.target).hide();

                    data.target.addClass("edit_mode_off").removeClass("edit_mode_on");
                    $(data.options.last_save_time_class,data.target).fadeOut();
            		data.target.trigger("genericFieldForm.toggle_off");
            	}
            	return false;
            })

        },
        save_and_status_btn_clicked: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericFieldForm');

                clearTimeout(data.form_save_timeout)
                data.target.genericFieldForm('save_form');
                return false;
            });
        },
        queue_form_save: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericFieldForm');

                // if any fields have changed
                var ser = $("input",data.form).serialize();

                if (data.previous_serialized_str != ser) {
                    data.previous_serialized_str = ser;
                    $(data.options.save_and_status_btn_class).html(data.options.save_now_text).addClass(data.options.save_now_class);
                    clearTimeout(data.form_save_timeout)
                    data.form_save_timeout = setTimeout(function(){data.target.genericFieldForm('save_form')}, 1500);
                }
            });
        },
        save_form: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericFieldForm');

                $(data.options.last_save_time_class).hide();
                $(data.options.last_save_time_class).html(data.options.last_saved_saving_text).fadeIn(50);
                $(data.options.save_and_status_btn_class).html(data.options.saving_text).removeClass(data.options.save_now_class);
                var save_start_time = new Date();
                $.ajax({
                  url: data.save_url,
                  type: data.save_method,
                  dataType: "json",
                  async: data.async,
                  data: $.param( $("input",data.form) ),
                	  success: function(json) {
                		$(".generic_editable_field",data.target).each(function(){
                			var field = $(this);
                			$(".view_field",field).html($(".edit_field input",field).val());
                		});
                		var savetime = new Date();
                		total_saving_time = savetime - save_start_time;
                		if (total_saving_time < data.options.min_save_message_display_time) {
                		    setTimeout(function(){data.target.genericFieldForm('show_saved_message')},data.options.min_save_message_display_time-total_saving_time);
                		} else {
                		    data.target.genericFieldForm('show_saved_message');
                		}
                	 },

                	  error: function() {
                		alert("error");
                	  }
                });
            });
        },
        show_saved_message: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericFieldForm');

                $(data.options.last_save_time_class).hide();
                $(data.options.last_save_time_class).html(data.options.saved_recently_text).fadeIn();
                setTimeout(function(){
                    $(data.options.save_and_status_btn_class).html(data.options.saved_text).removeClass(data.options.save_now_class);
                }, 200)
            });
        },
    };




    $.fn.genericFieldForm = function( method ) {
       if ( methods[method] ) {
         return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
       } else if ( typeof method === 'object' || ! method ) {
         return methods.init.apply( this, arguments );
       } else {
         $.error( 'Method ' +  method + ' does not exist on jQuery.genericFieldForm' );
       }    
     };
     
})(jQuery);

// Highlights
    $.Mycelium.highlight_search_terms = function(q, context_ele) {
    	var space_queries = q.split(" ");
    	highlight_regexes = [];
    	for (var j in space_queries) {
    		var q = space_queries[j];
    		if (q != "") {
    			highlight_regexes.push(new RegExp(q, "gi"));

    			var dash_queries = q.split("-");
    			if (dash_queries.length > 1) {
    				for (var k in dash_queries) {
    					if (dash_queries[k] != "") {
    						highlight_regexes.push(new RegExp(dash_queries[k], "gi"));
    					}
    				}
    			}
    		}
    	}
    	$(".highlightable", context_ele).each(function(){
    		var text = $(this).text();
    		for (var j in highlight_regexes) {
    			text = text.replace(highlight_regexes[j], '<b>$&</b>')
    		}
    		$(this).html(text);
    	});

    }

// Striping
    $.Mycelium.update_stripes = function(context_ele) {
        $(".striped .striped_row:even",context_ele).addClass("even");
        $(".striped .striped_row:odd",context_ele).addClass("odd");
    }
    $.Mycelium.update_stripes();

//  Mycelium Elements
    $("tabbed_box.with_button tab_title").live("click",function(){
        var box = $(this).parents("tabbed_box.with_button");
        if (box.hasClass("open")) {
            box.removeClass("open").addClass("closed");
            box.trigger("mycelium.tabbed_box.closed");
        } else {
            box.addClass("open").removeClass("closed");
            box.trigger("mycelium.tabbed_box.opened");
        }
    });
});

//Support Placeholders
$(document).ready(function() {
	if (!Modernizr.input.placeholder)
	{
		var placeholderText = $('#search').attr('placeholder');

		$('#search').attr('value',placeholderText);
		$('#search').addClass('placeholder');

		$('#search').focus(function() {
			if( ($('#search').val() == placeholderText) )
			{
				$('#search').attr('value','');
				$('#search').removeClass('placeholder');
			}
		});

		$('#search').blur(function() {
			if ( ($('#search').val() == placeholderText) || (($('#search').val() == '')) )
			{
				$('#search').addClass('placeholder');
				$('#search').attr('value',placeholderText);
			}
		});
	}
});