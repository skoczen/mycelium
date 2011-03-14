$(function(){
// Set up Mycelium object
	if ($.Mycelium === undefined) {
		$.Mycelium = new Object();
	}
	if (typeof(SEARCH_URL) == "undefined") {
	    var SEARCH_URL = "";
	}

// Fragments handler
	var fragments = new Object();
	
	fragments.options = {
	    json_dict_name: "fragments"
	};
	fragments.get_and_update_fragments = function(url, override_options) {
	    var default_options = {
          url: url,
          type: "POST",
          dataType: "json",
          success: function(json) {
             $.Mycelium.fragments.process_fragments_from_json(json);
          }
        };
        var options =  $.extend(default_options, override_options);
        $.ajax(options);
	};
	
    fragments.process_fragments_from_json = function(json) {
        if (json[fragments.options.json_dict_name] != undefined) {
            return fragments.process_fragments(json[fragments.options.json_dict_name]);
        } else {
            return fragments.process_fragments(json);
        }
    };
    
	fragments.process_fragments = function(fragment_dict) {
	    $("fragment").each(function(){
	        frag = $(this);
            if (fragment_dict[frag.attr("name")] != undefined) {
               frag.trigger("fragments."+frag.attr("action"), {'new_content':fragment_dict[frag.attr("name")], 'target':frag});
	        }
	    });
	    return true;
	};
	
	fragments.replace_content = function(e, d) {
        $(d.target).html(d.new_content);
	};
	fragments.append_content = function(e, new_content, target) {
	    $(target).append(new_content);
	};
	fragments.clear_content = function(e, new_content, target) {
        $(target).html("");
	};
    // Default fragment actions:
    // replace
    // append
    // clear
	$(document).bind("fragments.replace",fragments.replace_content);
	$(document).bind("fragments.append",fragments.append_content);
	$(document).bind("fragments.clear",fragments.clear_content);

	$.Mycelium.fragments = fragments;


	
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
               "saved_recently_text": "Saved a few seconds ago."
           };

           var options =  $.extend(defaults, options);

           return this.each(function() {
                var $this = $(this),
                    data = $this.data('genericFieldForm');
                
                
                if (!data) {
                    data = {};
                    data.options = options;
                    data.target = $this;
                    if (options.hasOwnProperty("form")) {
                        data.form = $(options.form);
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
                    $this.data('genericFieldForm',data);
                    data = $this.data('genericFieldForm');
                }

                data.form_save_timeout = null;
                data.previous_serialized_str = "";
                
                $(data.options.start_edit_btn_class,data.target).click(function(){data.target.genericFieldForm('toggle_edit');});
                $(data.options.done_edit_btn_class,data.target).click(function(){data.target.genericFieldForm('toggle_edit');});

                $("body").bind('keydown', 'ctrl+e',  function(){data.target.genericFieldForm('toggle_edit');});
                $("body").bind('keydown', 'alt+e',   function(){data.target.genericFieldForm('toggle_edit');});
                $("body").bind('keydown', 'meta+e',  function(){data.target.genericFieldForm('toggle_edit');});
                $("body").bind('keydown', 'meta+s',  function(){data.target.genericFieldForm('save_and_status_btn_clicked');});
                $("body").bind('keydown', 'ctrl+s',  function(){data.target.genericFieldForm('save_and_status_btn_clicked');});
                $("input").bind('keydown', 'meta+s', function(){data.target.genericFieldForm('save_and_status_btn_clicked');});
                $("input").bind('keydown', 'ctrl+s', function(){data.target.genericFieldForm('save_and_status_btn_clicked');});

                $(data.options.last_save_time_class,data.target).hide();
                $("input", data.target).live("change", function(){data.target.genericFieldForm('queue_form_save');});
                $("input", data.target).live("keyup",  function(){data.target.genericFieldForm('queue_form_save');});
                $("textarea", data.target).live("change", function(){data.target.genericFieldForm('queue_form_save');});
                $("textarea", data.target).live("keyup",  function(){data.target.genericFieldForm('queue_form_save');});
                $("select", data.target).live("change", function(){data.target.genericFieldForm('queue_form_save');});
                $("input", data.target).autoGrowInput({comfortZone: 30, resizeNow:true});

                $(data.options.save_and_status_btn_class, data.target).live("click", function(){data.target.genericFieldForm('save_and_status_btn_clicked');});

                data.previous_serialized_str = data.form.serialize();
                $this.data('genericFieldForm',data);
                
                // bind to window close, save if there's anything in the ajax queue
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
            });

        },
        save_and_status_btn_clicked: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericFieldForm');

                clearTimeout(data.form_save_timeout);
                data.target.genericFieldForm('save_form');
                return false;
            });
        },
        queue_form_save: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericFieldForm');

                // if any fields have changed
                var ser = $("input, select, textarea",data.form).serialize();

                if (data.previous_serialized_str != ser) {
                    data.previous_serialized_str = ser;
                    $(data.options.save_and_status_btn_class).html(data.options.save_now_text).addClass(data.options.save_now_class);
                    clearTimeout(data.form_save_timeout);
                    data.form_save_timeout = setTimeout(function(){data.target.genericFieldForm('save_form');}, 1500);
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
                $(data.form).ajaxSubmit({
                  url: data.save_url,
                  type: data.save_method,
                  dataType: "json",
                  async: data.async,
                  // data: $.param( $("input",data.form) ),
                	  success: function(json) {
                		$(".generic_editable_field",data.target).each(function(){
                			var field = $(this);
                			$(".view_field",field).html($(".edit_field input",field).val());
                		});
                		var savetime = new Date();
                		total_saving_time = savetime - save_start_time;
                		if (total_saving_time < data.options.min_save_message_display_time) {
                		    setTimeout(function(){data.target.genericFieldForm('show_saved_message');},data.options.min_save_message_display_time-total_saving_time);
                		} else {
                		    data.target.genericFieldForm('show_saved_message');
                		}
                	 },

                	  error: function() {
                	    console.log("error");
                        // alert("Error Saving.");
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
                }, 200);
            });
        }
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
        var has_single_b = false;
    	for (var j in space_queries) {
    		var q = space_queries[j];
    		if (q != "") {
                if (q == "<" || q == ">" || q == "/" || q == "b") {
                    if (q == "b") {
                        has_single_b = true;
                    }
                } else {
        			highlight_regexes.push(new RegExp(q, "gi"));
                }

    			var dash_queries = q.split("-");
    			if (dash_queries.length > 1) {
    				for (var k in dash_queries) {
    					if (dash_queries[k] != "") {
                            if (dash_queries[k] == "<" || dash_queries[k] == ">" || dash_queries[k] == "/" || dash_queries[k] == "b") {
                                if (dash_queries[k] == "b") {
                                    has_single_b = true;
                                }
                            } else {
                                highlight_regexes.push(new RegExp(dash_queries[k], "gi"));
                            }
    					}
    				}
    			}
    		}
    	}
    	$(".highlightable", context_ele).each(function(){
    		var text = $(this).text();
            if (has_single_b) {
                text = text.replace(new RegExp('b', "gi"), '<b>$&</b>');
            }
            for (var j in highlight_regexes) {
                text = text.replace(highlight_regexes[j], '<b>$&</b>');
    		}
            $(this).html(text);
    	});

    };

// Striping
    $.Mycelium.update_stripes = function(context_ele) {
        $(".striped .striped_row:even",context_ele).addClass("even");
        $(".striped .striped_row:odd",context_ele).addClass("odd");
    };
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