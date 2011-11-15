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
                    data.save_queued = false;
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
                $("input:not(.excluded_field)", data.target).live("change", function(){data.target.genericFieldForm('queue_form_save');});
                $("input:not(.excluded_field)", data.target).live("keyup",  function(){data.target.genericFieldForm('queue_form_save');});
                $("textarea:not(.excluded_field)", data.target).live("change", function(){data.target.genericFieldForm('queue_form_save');});
                $("textarea:not(.excluded_field)", data.target).live("keyup",  function(){data.target.genericFieldForm('queue_form_save');});
                $("select:not(.excluded_field)", data.target).live("change", function(){data.target.genericFieldForm('queue_form_save');});
                $("input", data.target).autoGrowInput({comfortZone: 30, resizeNow:true});

                $(data.options.save_and_status_btn_class, data.target).live("click", function(){data.target.genericFieldForm('save_and_status_btn_clicked');});

                data.previous_serialized_str = data.form.serialize();
                $this.data('genericFieldForm',data);
                
                // bind to window close, save if there's anything in the ajax queue
                $(window).bind("unload.genericFieldForm",function(){
                	if (data.save_queued) {
                		clearTimeout(data.form_save_timeout);
                    	data.async = false;
                    	data.target.genericFieldForm('save_form');                		
                	}
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
                	// mark it as dirty
	                data.target.addClass("dirty");

                	data.save_queued = true;
                    data.previous_serialized_str = ser;
                    $(data.options.save_and_status_btn_class).html(data.options.save_now_text).addClass(data.options.save_now_class);
                    clearTimeout(data.form_save_timeout);
                    data.form_save_timeout = setTimeout(function(){data.target.genericFieldForm('save_form');}, 1500);
                    data.target.trigger("genericFieldForm.queue_form_save");
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
                data.target.removeClass("dirty");
                $(data.form).ajaxSubmit({
                  url: data.save_url,
                  type: data.save_method,
                  dataType: "json",
                  async: data.async,
                  // data: $.param( $("input",data.form) ),
                	  success: function(json) {
                	  	data.save_queued = false;
                		$(".generic_editable_field",data.target).each(function(){
                			var field = $(this);
                			if ($(".edit_field select",field).length > 0) {
                				$(".view_field",field).html($(".edit_field select option:selected",field).text());	
                			} else {
                				if ($(".edit_field input[type=radio]:checked",field).length > 0 ) {
                					$(".view_field",field).html($(".edit_field label[for="+$(".edit_field input[type=radio]:checked").attr("id")+"]").html());
                				} else {
                					$(".view_field",field).html($(".edit_field input, .edit_field textarea",field).val());		
                				}
                				
                			}
                			
                		});
                		var savetime = new Date();
                		total_saving_time = savetime - save_start_time;
                		if (total_saving_time < data.options.min_save_message_display_time) {
                		    setTimeout(function(){data.target.genericFieldForm('show_saved_message');},data.options.min_save_message_display_time-total_saving_time);
                		} else {
                		    data.target.genericFieldForm('show_saved_message');
                		}
                		data.target.trigger("genericFieldForm.save_form_success");
                	 },

                	  error: function() {
                	  	data.save_queued = false;
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