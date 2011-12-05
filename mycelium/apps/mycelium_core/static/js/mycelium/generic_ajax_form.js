if (! Object.hasOwnProperty("size")) {
	Object.size = function(obj) {
	    var size = 0, key;
	    for (key in obj) {
	        if (obj.hasOwnProperty(key)) size++;
	    }
	    return size;
	};
}
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

// Save works.  Queuing, new, delete, etc don't yet.  Do those next.


	var PageObject = function(form_object, db_pk, target) {
		var o = {};
		o.form_object = form_object;
		o.target = target;
		o.form_object_type = target.attr("form_object_type");
		o.page_pk = $.fn.genericAjaxGetNextPagePk();
		target.attr("page_pk", o.page_pk);
		o.db_pk = db_pk;
		o.new_in_progress = false;
		o.waiting_on_db_pk = false;
		o.save_queued = false;
		o.save_in_progress = false;
		o.deleted = false;
		o.delete_queued = false;
		o.delete_in_progress = false;
		o.save_key = function() {
			return this.form_object_type + "-" + this.page_pk;
		}
		o.delete_key = function() {
			return this.form_object_type + "-" + this.page_pk + "delete";
		}
		o.get_data = function(){return this.form_object.get_data(this)};

		o.save = function() {
			
		}
		o.serialized_string = function(){return $("input, select, textarea",this.target).serialize();}
		o.previous_serialized_str = o.serialized_string();
		o.has_changed = function() {
			return this.previous_serialized_str != this.serialized_string()
		}
		o.update_serialized_string = function() {
			this.previous_serialized_str = this.serialized_string();
		}
		o.start_save = function() {
			this.save_in_progress = true;
		}
		o.finish_save = function() {
			this.save_in_progress = false;
		}
		o.queue_save = function() {
			this.save_queued = true;
		}
		o.dequeue_save = function() {
			this.save_queued = false;
		}
		o.start_delete = function(context, data) {
			this.delete_in_progress = true;
			this.target.hide();
			data.add_to_save_queue(this.delete_key());
			$.ajax({
              url: this.form_object.delete_object_url,
              type: data.save_method,
              dataType: "json",
              async: data.async,
              data: this.get_data(),
              success: function(json){return data.target.genericAjaxForm('delete_object_response', context, json) },
              error: function(){this.target.show(); alert("Error deleting. Please refresh the page, and try again. Sorry!")}
            });	
		}
		o.finish_delete = function(data) {
			this.delete_in_progress = false;
			data.remove_from_save_queue(this.delete_key());
			this.target.remove();
		}
		o.queue_delete = function() {
			this.delete_queued = true;
		}
		o.start_new = function() {
			this.new_in_progress = true;
			this.save_in_progress = true;
			this.waiting_on_db_pk = true;
		}
		o.finish_new = function(json) {
			this.db_pk = json.db_pk;
			this.target.attr("db_pk", this.db_pk).attr("pk", this.db_pk)
			this.waiting_on_db_pk = false;
			this.save_in_progress = false;
			this.new_in_progress = false;
		}
		return o;
	};
	var SaveQueueItem = function(form_object) {
		this.form_object = form_object;
	};
	var createPageObjectFromCanonical = function(form_object, form_object_name, selector) {
			var objs = {}
			$(selector).each(function(){
				var obj_pk = $(this).attr("pk");
				obj_pk = (obj_pk == "") ? false : obj_pk;
				var po = PageObject(form_object, obj_pk, $(this))
				objs[form_object_name+"_"+po.page_pk] = po;
			});
			return objs
	};
	var getFormFieldData = function(target) {
		return $(target).formToArray(true)
	};

	var get_page_object = function(data, object_name, page_pk) {
		return (data.page_objects.hasOwnProperty(object_name+"_"+page_pk)) ? data.page_objects[(object_name+"_"+page_pk)] : false;
	};

    $.fn.genericAjaxGetNextPagePk = function() {
		if ($.genericAjaxPagePk == undefined) {
			$.genericAjaxPagePk = 0;
		}
		$.genericAjaxPagePk++;
		return $.genericAjaxPagePk;
    };


    var methods = {
       init : function( opt ) {
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

           var options =  $.extend(defaults, opt);

           return this.each(function() {
                var $this = $(this),
                    data = $this.data('genericAjaxForm');
                
                
                if (!data) {
                    data = {};
                    data.options = options;
                    data.target = $this;
                    data.custom_save_mode = false;

                    if (opt.hasOwnProperty("form_objects")) {
						data.custom_save_mode = true;
						$this.data('genericAjaxForm',data);
						data = $this.data('genericAjaxForm');
                    	data.form_objects = data.options.form_objects;
                    	data.page_objects = {};
                    	data.save_queue = {};
                    	data.page_pk = 1;
						data.add_to_save_queue = function (key) {
							this.save_queue[key] = true;
						}
                    	data.remove_from_save_queue = function(key) {
            				delete this.save_queue[key];
            			}
                    		// - key is object_name+"_"+page_pk
							// - value is the SaveQueueItem
                    	for (var key in data.form_objects) {
                    		var fo = data.form_objects[key]
                    		var selector = "."+key+".canonical";
                    		var target = $(selector);
                    		if (!fo.hasOwnProperty('get_objects')) {
                    			fo.get_objects = function(){ return createPageObjectFromCanonical(this, key, selector)};
                    		}
                    		if (!fo.hasOwnProperty('get_data')) {
                    			fo.get_data = function(page_object){ 
	                    			var o = {};
                    				var d = getFormFieldData(page_object.target);
                    				for (var j=0; j<d.length; j++) {
                    					var k = d[j]["name"];
                    					if (page_object.form_object.hasOwnProperty('django_formset_prefix')) {
                    						if (k.indexOf(page_object.form_object.django_formset_prefix+"-") != -1) {
												// Slice off the formset name prefixes
												var first_dash = k.indexOf(page_object.form_object.django_formset_prefix+"-")+page_object.form_object.django_formset_prefix.length+1
                    							k = k.slice(0,first_dash) + k.slice(k.indexOf("-", first_dash+1)+1)
                    						}
                    					}
                    					o[k] = d[j]["value"];
                    				}
                    				o["page_pk"]= page_object.page_pk;
                    				o["db_pk"]= page_object.db_pk;
                    				o["form_object_type"] = page_object.form_object_type;
                    				// Get all parent canonicals, put their pks in.
                    				page_object.target.parents(".canonical").each(function() {
                    					var par = $(this);
                    					o[par.attr("form_object_type")+"_pk"] = par.attr("pk")
                    				})
                    				return o
                    			};
                    		}
                    		data.page_objects = $.extend(data.page_objects,fo.get_objects())
                    	}
                	
                	}
                	
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
                $("input:not(.excluded_field)", data.target).live("change", function(){data.target.genericAjaxForm('queue_form_save', $(this), data.target);});
                $("input:not(.excluded_field)", data.target).live("keyup",  function(){data.target.genericAjaxForm('queue_form_save', $(this), data.target);});
                $("textarea:not(.excluded_field)", data.target).live("change", function(){data.target.genericAjaxForm('queue_form_save', $(this), data.target);});
                $("textarea:not(.excluded_field)", data.target).live("keyup",  function(){data.target.genericAjaxForm('queue_form_save', $(this), data.target);});
                $("select:not(.excluded_field)", data.target).live("change", function(){data.target.genericAjaxForm('queue_form_save', $(this), data.target);});
                $("input", data.target).autoGrowInput({comfortZone: 30, resizeNow:true});

                $(data.options.save_and_status_btn_class, data.target).live("click", function(){data.target.genericAjaxForm('save_and_status_btn_clicked');});

                data.previous_serialized_str = data.form.serialize();
                $this.data('genericAjaxForm',data);
                
                // bind to window close, save if there's anything in the ajax queue
                $(window).bind("beforeunload.genericAjaxForm", function() {
                	if (data.custom_save_mode) {
                		if (Object.size(data.save_queue) != 0) {
                			return "Changes are still being saved. Are you sure you want to leave the page, and lose your changes?"
                		}
                	} else {
	                	if (data.save_queued) {
							return "Changes are still being saved. Are you sure you want to leave the page, and lose your changes?";
	                	}	
                	}
                	return 
	            });
                $(window).bind("unload.genericAjaxForm",function(){
                	if (data.custom_save_mode) {
                		if (Object.size(data.save_queue) != 0) {
                			return false;
                		}
                	} else {
	                	if (data.save_queued) {
	                		clearTimeout(data.form_save_timeout);
	                    	data.async = false;
	                    	data.target.genericAjaxForm('save_form');                		
	                	}	
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
                var $this = $(this), data = $this.data('genericAjaxForm');
            	clearTimeout(data.form_save_timeout);
            	data.target.genericAjaxForm('save_form');	
                return false;
            });
        },
        queue_form_save: function(target, data_target){
            return $(target).each(function(){
                var $this = $(data_target),
                    data = $this.data('genericAjaxForm');

                if (data.custom_save_mode) {
                	page_object = get_page_object(data, $(target).parents(".canonical").attr("form_object_type"), $(target).parents(".canonical").attr("page_pk"));
                	if (page_object.has_changed()) {
						if ($(data.options.last_save_time_class).html() != data.options.last_saved_saving_text) {
							data.target.genericAjaxForm('show_saving_message');
						}
						
                		if (page_object.save_in_progress) {
                			page_object.queue_save()
                		} else {
                			data.target.genericAjaxForm('save_object', $this, page_object, data.target);	
                		}
                	}
                } else {
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
	                    data.target.trigger("genericAjaxForm.queue_form_save", $(target), data);
	                }                	
                }

                
            });
        },
        save_form: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericAjaxForm');

                data.target.genericAjaxForm('show_saving_message');
                var save_start_time = new Date();
                data.target.removeClass("dirty");

                if (data.custom_save_mode) {
                	// console.log("custom save")
                } else {
	                
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
                }
               
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
        show_saving_message: function(){
            return $(this).each(function(){
                var $this = $(this),
                    data = $this.data('genericAjaxForm');

				$(data.options.last_save_time_class).hide();
				$(data.options.last_save_time_class).html(data.options.last_saved_saving_text).fadeIn(50);
				$(data.options.save_and_status_btn_class).html(data.options.saving_text).removeClass(data.options.save_now_class);
            });
        },
		get_form_object: function(object_name) {
			var $this = $(this), data = $this.data('genericAjaxForm');
			return data.form_objects[object_name];
		},
		save_object: function(context, page_object) {
			if (page_object.db_pk != false) {
				var $this = $(context), data = $this.data('genericAjaxForm');
				data.add_to_save_queue(page_object.save_key());
				page_object.update_serialized_string()
				page_object.start_save();
				$.ajax({
	              url: page_object.form_object.save_object_url,
	              type: data.save_method,
	              dataType: "json",
	              async: data.async,
	              data: page_object.get_data(),
	              success: function(json){return data.target.genericAjaxForm('save_object_response', context, json) }
	            });		
			}
		},
		save_object_response: function(context, json) {
			var $this = $(context), data = $this.data('genericAjaxForm');
			
			page_object = get_page_object(data, json.form_object_type, json.page_pk);
			page_object.finish_save();
			
			data.target.genericAjaxForm('handle_queued_actions', $this, page_object);

			// - Check waiting_on_db_pk.  If true, set the db_pk.
			// - Check waiting_to_delete.  If set, call delete.
			// - Check the PendingSaveQueue, drop the key and trigger a new save if it contains a key for this FormObject.
			// - GenericAjaxForm.trigger("saved_object", object_type, page_pk)			
		},

		new_object: function(context, object_name, target) {
			var $this = $(context).genericAjaxForm('self'), data = $this.data('genericAjaxForm');
			var page_objects = createPageObjectFromCanonical(data.form_objects[object_name], object_name, target)
			data.page_objects = $.extend(data.page_objects,page_objects)

			data.target.genericAjaxForm('show_saving_message');

			for (key in page_objects) {
	     	   page_object = page_objects[key];
	    	}
			page_object.start_new();

			$.ajax({
              url: page_object.form_object.new_object_url,
              type: data.save_method,
              dataType: "json",
              async: data.async,
              data: page_object.get_data(),
              success: function(json){return data.target.genericAjaxForm('new_object_response', context, json) }
              // success: function() {alert("bar")}
            });	
			data.target.genericAjaxForm('save_object', $this, page_object);
			
		},
		new_object_response: function(context, json) {
			var $this = $(context), data = $this.data('genericAjaxForm');
			
			page_object = get_page_object(data, json.form_object_type, json.page_pk);
			page_object.finish_new(json);
			data.target.genericAjaxForm('handle_queued_actions', $this, page_object);
		
		},
		delete_object: function(context, target) {
			var $this = $(context), data = $this.data('genericAjaxForm');
			page_object = get_page_object(data, $(target).parents(".canonical").attr("form_object_type"), $(target).parents(".canonical").attr("page_pk"));
			data.target.genericAjaxForm('show_saving_message');

			if (page_object.save_in_progress) {
				page_object.queue_delete();
			} else {
				page_object.start_delete(context, data);	
			}
		},
		delete_object_response: function(context, json) {
			var $this = $(context), data = $this.data('genericAjaxForm');
			page_object = get_page_object(data, json.form_object_type, json.page_pk);
			page_object.finish_delete(data);

			data.target.genericAjaxForm('handle_queued_actions', $this, page_object);
		},
		handle_queued_actions: function(context, page_object) {
			var savetime = new Date();

			var $this = $(context), data = $this.data('genericAjaxForm');
			data.remove_from_save_queue(page_object.save_key());

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

			if (page_object.delete_queued) { 
				data.target.genericAjaxForm('delete_object', $this, context, data.target);
			} else {
				if (page_object.save_queued) {
					page_object.dequeue_save()
					data.target.genericAjaxForm('save_object', $this, page_object, data.target);
				}	
			}

			if (Object.size(data.save_queue) == 0) {
				data.target.genericAjaxForm('show_saved_message');
	    		data.target.trigger("genericAjaxForm.save_form_success");
			}
		},
		form_objects: function(){
			var $this = $(this), data = $this.data('genericAjaxForm');
			return data.form_objects;
		},
		self: function(){
			return $(this);
		}
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


})(jQuery);