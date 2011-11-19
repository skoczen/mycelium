// Generic Ajax Form
(function($){
	/*
	 Two modes:
	 	Simple.  $("#form_id").genericAjaxForm() will save anytime form fields are changed, by ajax posting to the form URL, queuing changes, and updating the save as needed.
	 	Advanced. $("#form_id").genericAjaxForm({'form_objects':{}}) is for complex, fk-related forms/formsets, including add/delete.


	Basic Ideas:
	- Backend agnostic.  However, the backend must respond to the following POST/JSON-reponses:

		save_object 
			POSTs:
				page_pk:  an int, unique to this page/pageload
				db_pk: is the db pk, if known
				data: the remainder of the form data to save
			Response (JSON):
				page_pk: the same int
				db_pk: the same pk
				event_success: boolean
				error_string: descriptive, user-facing. only if success==false.
		
		new_object
			POSTs:
				page_pk:  an int, unique to this page/pageload
				data: the remainder of the form data to save
			Response (JSON):
				page_pk: the same int
				db_pk: the pk given by the db
				event_success: boolean
				error_string: descriptive, user-facing. only if success==false.

		delete_object
			POSTs:
				page_pk:  an int, unique to this page/pageload
				db_pk: is the db pk, if known
			Response (JSON):
				page_pk: the same int
				db_pk: the same pk
				event_success: boolean
				error_string: descriptive, user-facing. only if success==false.

	- The client always wins.
		The client holds the canonical data structure, and is responsible for making sure the backend knows the proper state.  
		This includes edge cases like pk-creation race conditions, creation/deletion races, and an attempt at browser-crash/close states.

	
	- Client abstraction:
		FormObject:
			- object_name (string)
			- page_pk (int, unique)
			- db_pk (null / arbitrary)
			- waiting_on_db_pk (boolean)
			- wating_to_delete (boolean)
			- deleted (boolean)
			- get_data (function)
		SaveQueueItem
			- form_object
		SaveQueue(Dict)
			- key is object_name+"_"+page_pk
			- value is the SaveQueueItem
		PendingSaveQueue(Dict)
			- key is object_name+"_"+page_pk
			- value is the SaveQueueItem
		form_object_types = []
		
	- Client event reponses:
		To save_object:
			- Check waiting_on_db_pk.  If true, set the db_pk.
			- Check waiting_to_delete.  If set, call delete.
			- Check the PendingSaveQueue, drop the key and trigger a new save if it contains a key for this FormObject.
			- GenericAjaxForm.trigger("saved_object", object_type, page_pk)
		To new_object:
			- Same as save_object
			- GenericAjaxForm.trigger("new_object", object_type, page_pk)
		To delete_object:
			- deleted was set on submit
			- delete the FormObject
			- GenericAjaxForm.trigger("deleted_object", object_type, page_pk)


	- Usage:
		var form_options = {
			form_objects: {
				"person": {
					get_objects: function(){ 
										// Initially gets the set of objects from the page body.
										},
					get_data: function(){ 
										// Gets data prior to ajax POST. 
										},
					save_object_url: "/person/save",
					new_object_url: "/person/new",
					delete_object_url: "/person/delete"
				},
				"phone_number": {
					get_objects: function(){ 
										// Initially gets the set of objects from the page body.
										},
					get_data: function(){ 
										// Gets data prior to ajax POST. 
										},
					save_object_url: "/phone_number/save",
					new_object_url: "/phone_number/new",
					delete_object_url: "/phone_number/delete"			
				},
				"email": {
					get_objects: function(){ 
										// Initially gets the set of objects from the page body.
										},
					get_data: function(){ 
										// Gets data prior to ajax POST. 
										},
					save_object_url: "/email/save",
					new_object_url: "/email/new",
					delete_object_url: "/email/delete"			
				}
			}
		}

		$("#basic_info_form").genericAjaxForm(form_options);

	*/




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
           };

           var options =  $.extend(defaults, options);

           return this.each(function() {
                var $this = $(this),
                    data = $this.data('genericAjaxForm');
                
                
                if (!data) {
                    data = {};
                    data.options = options;
                    data.target = $this;
                    if (data.options.hasOwnProperty("form_objects")) {
						data.custom_save_mode = true;
						$this.data('genericAjaxForm',data);
						data = $this.data('genericAjaxForm');
                    	data.form_objects = data.options.form_objects;
                    	data.page_objects = {};
                    	data.save_queue = {};
                    	data.page_pk = 1;
                    	data.pending_save_queue = {};
                    		// - key is object_name+"_"+page_pk
							// - value is the SaveQueueItem
                    	for (var key in data.form_objects) {
                    		var fo = data.form_objects[key]
                    		data.page_objects[key] = fo.get_objects()
                    	}
                    	console.log(data.page_objects)
                    } else {
                    	data.custom_save_mode = false;
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
                    }
                    
                    $this.data('genericAjaxForm',data);
                    data = $this.data('genericAjaxForm');
                }

                data.form_save_timeout = null;
                data.previous_serialized_str = "";
                
                $(data.options.start_edit_btn_class,data.target).click(function(){data.target.genericAjaxForm('toggle_edit');});
                $(data.options.done_edit_btn_class,data.target).click(function(){data.target.genericAjaxForm('toggle_edit');});

                $("body").bind('keydown', 'ctrl+e',  function(){data.target.genericAjaxForm('toggle_edit');});
                $("body").bind('keydown', 'alt+e',   function(){data.target.genericAjaxForm('toggle_edit');});
                $("body").bind('keydown', 'meta+e',  function(){data.target.genericAjaxForm('toggle_edit');});
                $("body").bind('keydown', 'meta+s',  function(){data.target.genericAjaxForm('save_and_status_btn_clicked');});
                $("body").bind('keydown', 'ctrl+s',  function(){data.target.genericAjaxForm('save_and_status_btn_clicked');});
                $("input").bind('keydown', 'meta+s', function(){data.target.genericAjaxForm('save_and_status_btn_clicked');});
                $("input").bind('keydown', 'ctrl+s', function(){data.target.genericAjaxForm('save_and_status_btn_clicked');});

                $(data.options.last_save_time_class,data.target).hide();
                $("input:not(.excluded_field)", data.target).live("change", function(){data.target.genericAjaxForm('queue_form_save');});
                $("input:not(.excluded_field)", data.target).live("keyup",  function(){data.target.genericAjaxForm('queue_form_save');});
                $("textarea:not(.excluded_field)", data.target).live("change", function(){data.target.genericAjaxForm('queue_form_save');});
                $("textarea:not(.excluded_field)", data.target).live("keyup",  function(){data.target.genericAjaxForm('queue_form_save');});
                $("select:not(.excluded_field)", data.target).live("change", function(){data.target.genericAjaxForm('queue_form_save');});
                $("input", data.target).autoGrowInput({comfortZone: 30, resizeNow:true});

                $(data.options.save_and_status_btn_class, data.target).live("click", function(){data.target.genericAjaxForm('save_and_status_btn_clicked');});

                data.previous_serialized_str = data.form.serialize();
                $this.data('genericAjaxForm',data);
                
                // bind to window close, save if there's anything in the ajax queue
                $(window).bind("unload.genericAjaxForm",function(){
                	if (data.save_queued) {
                		clearTimeout(data.form_save_timeout);
                    	data.async = false;
                    	data.target.genericAjaxForm('save_form');                		
                	}
                });
            });
        },
        
        toggle_edit: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericAjaxForm');
                
            	if (data.target.hasClass("edit_mode_off")) {
            		$(data.options.save_and_status_btn_class,data.target).show();
            		$(data.options.start_edit_btn_class,data.target).hide();
            		$(data.options.done_edit_btn_class,data.target).show();

                    data.target.removeClass("edit_mode_off").addClass("edit_mode_on");
            		$(data.options.last_save_time_class,data.target).fadeIn();
            		data.target.trigger("genericAjaxForm.toggle_on");
            	} else {
            		$(data.options.save_and_status_btn_class,data.target).hide();
            		$(data.options.start_edit_btn_class,data.target).show();
            		$(data.options.done_edit_btn_class,data.target).hide();

                    data.target.addClass("edit_mode_off").removeClass("edit_mode_on");
                    $(data.options.last_save_time_class,data.target).fadeOut();
            		data.target.trigger("genericAjaxForm.toggle_off");
            	}
            	return false;
            });

        },
        save_and_status_btn_clicked: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericAjaxForm');

                clearTimeout(data.form_save_timeout);
                data.target.genericAjaxForm('save_form');
                return false;
            });
        },
        queue_form_save: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericAjaxForm');
                   
                // if any fields have changed
                var ser = $("input, select, textarea",data.form).serialize();

                if (data.previous_serialized_str != ser) {
                	// mark it as dirty
	                data.target.addClass("dirty");

                	data.save_queued = true;
                    data.previous_serialized_str = ser;
                    $(data.options.save_and_status_btn_class).html(data.options.save_now_text).addClass(data.options.save_now_class);
                    clearTimeout(data.form_save_timeout);
                    data.form_save_timeout = setTimeout(function(){data.target.genericAjaxForm('save_form');}, 1500);
                    data.target.trigger("genericAjaxForm.queue_form_save");
                }
                
            });
        },
        save_form: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericAjaxForm');

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
                		    setTimeout(function(){data.target.genericAjaxForm('show_saved_message');},data.options.min_save_message_display_time-total_saving_time);
                		} else {
                		    data.target.genericAjaxForm('show_saved_message');
                		}
                		data.target.trigger("genericAjaxForm.save_form_success");
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
                    data = $this.data('genericAjaxForm');

                $(data.options.last_save_time_class).hide();
                $(data.options.last_save_time_class).html(data.options.saved_recently_text).fadeIn();
                setTimeout(function(){
                    $(data.options.save_and_status_btn_class).html(data.options.saved_text).removeClass(data.options.save_now_class);
                }, 200);
            });
        },
		get_form_object: function(object_name) {
			var $this = $(this), data = $this.data('genericAjaxForm');
			return data.form_objects[object_name];
		},
		get_page_object: function(object_name, page_pk) {
			var $this = $(this), data = $this.data('genericAjaxForm');
			return (data.page_objects.hasOwnProperty(object_name+"_"+page_pk)) ? data.form_objects[(object_name+"_"+page_pk)] : false;
		},
		save_object: function(object_name, page_pk) {
			var $this = $(this), data = $this.data('genericAjaxForm');
			var fo = data.target.genericAjaxForm('get_page_object')(object_name, page_pk);
			console.log(fo)

		},
		save_object_response: function(json) {
			var $this = $(this), data = $this.data('genericAjaxForm');
			// - Check waiting_on_db_pk.  If true, set the db_pk.
			// - Check waiting_to_delete.  If set, call delete.
			// - Check the PendingSaveQueue, drop the key and trigger a new save if it contains a key for this FormObject.
			// - GenericAjaxForm.trigger("saved_object", object_type, page_pk)			
		},

		new_object: function(object_name, page_pk) {
			var $this = $(this), data = $this.data('genericAjaxForm');
			
		},
		new_object_response: function(json) {
			var $this = $(this), data = $this.data('genericAjaxForm');
			// - Same as save_object
			// - GenericAjaxForm.trigger("new_object", object_type, page_pk)			
		},

		delete_object: function(object_name, page_pk) {
			var $this = $(this), data = $this.data('genericAjaxForm');
			
		},
		delete_object_response: function(json) {
			var $this = $(this), data = $this.data('genericAjaxForm');
			// - deleted was set on submit
			// - delete the FormObject
			// - GenericAjaxForm.trigger("deleted_object", object_type, page_pk)			
		},
    };


    $.fn.genericAjaxForm = function( method ) {
       if ( methods[method] ) {
         return methods[method].apply( this, Array.prototype.slice.call( arguments, 1 ));
       } else if ( typeof method === 'object' || ! method ) {
         return methods.init.apply( this, arguments );
       } else {
         $.error( 'Method ' +  method + ' does not exist on jQuery.genericAjaxForm' );
       }    
    };

	$.fn.genericAjaxFormClasses = function( method ) {
		return {
			PageObject: function(form_object, db_pk) {
				var $this = $(this), data = $this.data('genericAjaxForm');
				var o = {};
				o.form_object = form_object;
				o.page_pk = $.fn.genericAjaxGetNextPagePk();
				o.db_pk = db_pk;
				o.waiting_on_db_pk = false;
				o.wating_to_delete = false;
				o.deleted = false;
				o.get_data = form_object.get_data;
				return o;
			},
			SaveQueueItem: function(form_object) {
				this.form_object = form_object;
			},
			createPageObjectFromCanonical: function(form_object, selector) {
					var objs = []
					$(selector).each(function(){
						var obj_pk = $(selector).attr("pk");
						var ph = $.fn.genericAjaxFormClasses().PageObject(form_object, obj_pk)
						objs.push(ph)
					});
					return objs
			}
		}
	};
    $.fn.genericAjaxGetNextPagePk = function() {
		if ($.genericAjaxPagePk == undefined) {
			$.genericAjaxPagePk = 0;
		}
		$.genericAjaxPagePk++;
		return $.genericAjaxPagePk
    };


})(jQuery);