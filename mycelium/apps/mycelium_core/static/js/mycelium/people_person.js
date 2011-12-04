$(function(){
	personPage.init();
});

var personPage = {};
personPage.tag_fadeout_timeout = false;
personPage.prev_tab_name = "#recent_activity";

personPage.init = function() {
	// $("#phone_number_form_container .phone_number_canonical_container:last").hide();
	// $("#email_form_container .email_canonical_container:last").hide();

	personPage.create_blank_element("phone_number", "New phone");
	personPage.create_blank_element("email", "New email");
	$(".delete_email_btn").live("click", personPage.delete_email);
	$(".delete_phone_number_btn").live("click", personPage.delete_phone_number);
	$(".primary_radio").live("click",personPage.primary_clicked);
	


	// input.val("").attr("placeholder", "Add an email");
	// personPage.convert_zero_elements_to_blank(input);
	// $(".phone_number.blank .number .view_field").html("");
	// $("#phone_number_blank_container .number input").live("change", personPage.blank_phone_number_changed);


    $(".person_delete_btn").click(personPage.delete_person);
    $("detail_tabs a.detail_tab").live("click",personPage.detail_tab_clicked);
    $(".general_person_tags").genericTags();
    var default_tab = $.bbq.getState('current_detail_tab');
    if (default_tab !== undefined) {
        load_detail_tab(default_tab);
    }
};

personPage.create_blank_element = function(element_name, placeholder) {
	// var first = $("#"+element_name+"_form_container ."+element_name+"_canonical_container");
	var input = $("."+element_name+"_canonical_container .number input");
	if ($("#"+element_name+"_form_container ."+element_name+"_canonical_container").length <= 1 && input.val() == "") {
		input.bind("keyup.new_field",function(){return personPage.blank_element_changed($(this), element_name, placeholder)});			
		input.attr("placeholder", placeholder).css("min-width", "120px");
	} else {
		if ($("#"+element_name+"_form_container ."+element_name+"_canonical_container").length == 1) {
			$("."+element_name+"_canonical_container:first .number input").attr("placeholder", "");
		}
		var blank = $("#"+element_name+"_form_container ."+element_name+"_canonical_container:first").clone();
		$("#"+element_name+"_form_container").append("<span class='"+element_name+"_canonical_container blank'></span>");
		
		$("input, select", blank).addClass("excluded_field");
		$("."+element_name+".canonical", blank).attr("pk", "").attr("page_pk", "");
		$(".contact_type, .primary, .delete", blank).html("");
		$(".number input", blank).val("").attr("placeholder", placeholder);
		$(".number .view_field", blank).html("");

		personPage.convert_zero_elements_to_blank($(".number input", blank));

		$("."+element_name+"_canonical_container.blank").append(blank.children());
		
		$("."+element_name+"_canonical_container .number input").unbind("keyup.new_field");
		$("."+element_name+"_canonical_container.blank .number input").bind("keyup.new_field",function(){return personPage.blank_element_changed($(this), element_name, placeholder)});			
	}
	
	personPage.ensure_last_element_cant_be_deleted(element_name);
	
	
}
personPage.convert_zero_elements_to_blank = function(ele) {
	$(ele).each(function(){
		var e = $(this);
		e.attr("name", e.attr("name").replace("-0-","-BLANK-"));
		e.attr("id", e.attr("id").replace("-0-","-BLANK-"));
		if (e.attr("for") != undefined) {
			e.attr("for", e.attr("for").replace("-0-","-BLANK-"));
		}
		try {
			if (e.attr("type") == "checkbox"){
				e.removeAttr("checked");	
			} else {
				e.val("");
			}
			
		} catch(e) {}
	});
}
personPage.convert_blank_elements_to_new = function(ele, counter) {
	$(ele).each(function(){
		var e = $(this);
		e.attr("name", e.attr("name").replace("-BLANK-", "-"+counter+"-"));
		e.attr("id", e.attr("id").replace("-BLANK-", "-"+counter+"-"));
		if (e.attr("for") != undefined) {
			e.attr("for", e.attr("for").replace("-BLANK-", "-"+counter+"-"));	
		}
		
	});
}
personPage.cloned_and_cleared = function(ele) {
	var e = ele.clone()
	try {
		$("select, input",e).val("").addClass("excluded_field");
	} catch(e) {}
	personPage.convert_zero_elements_to_blank($("select, input, label",e));
	return e.html();
}

personPage.blank_element_changed = function(target, element_name, placeholder) {
	var ele = $(target);
	if (ele.val() != "") {
		// Make a new one, initialize the fields.
		var num_elements = $("#"+element_name+"_form_container ."+element_name+".canonical").length;
		$("."+element_name+"_canonical_container.blank .contact_type").html(personPage.cloned_and_cleared($("#"+element_name+"_form_container .contact_type:first")));
		$("."+element_name+"_canonical_container.blank .primary").html(personPage.cloned_and_cleared($("#"+element_name+"_form_container .primary:first")));
		$("."+element_name+"_canonical_container.blank .delete").html(personPage.cloned_and_cleared($("#"+element_name+"_form_container .delete:first"))).show();
		$("."+element_name+"_canonical_container.blank .canonical").removeClass("is_primary");
		$("."+element_name+"_canonical_container.blank .primary .faux_radio").removeClass("checked");

		personPage.convert_blank_elements_to_new( $("select, input, label", $("."+element_name+"_canonical_container.blank")), num_elements);

		// Add to form_objects.
		$("#basic_info_form").genericAjaxForm('new_object', "#basic_info_form", element_name, $("."+element_name+"_canonical_container.blank .canonical"));

		$("."+element_name+"_canonical_container.blank input, ."+element_name+"_canonical_container.blank select").removeClass("excluded_field");
		$("."+element_name+"_canonical_container.blank .number input").unbind("keyup.new_field");
		$("."+element_name+"_canonical_container.blank").removeClass("blank");

		personPage.create_blank_element(element_name, placeholder);
	}
	return false;
}
personPage.delete_element = function(target, element_name) {
	var ele = $(target);
	ele.parents("."+element_name+"_canonical_container").addClass("pre_delete");
	setTimeout(function(){
		if ($(".number input", ele).val() == "" || confirm("Are you sure you want to remove this "+element_name.replace("_"," ")+"?")) {
			$("#basic_info_form").genericAjaxForm('delete_object', "#basic_info_form", ele);
			personPage.ensure_last_element_cant_be_deleted(element_name);
		} else {
			ele.parents("."+element_name+"_canonical_container").removeClass("pre_delete");
		}
	}, 50);

}

personPage.ensure_last_element_cant_be_deleted = function(element_name) {
	var first = $("#"+element_name+"_form_container ."+element_name+"_canonical_container:not(.blank):not(.pre_delete)");
	$(".delete", first).hide();

	console.log("#"+element_name+"_form_container ."+element_name+"_canonical_container:not(.blank):not(.pre_delete)")
	console.log("first.length")
	console.log(first.length)
	if (first.length <= 1) {
		$(".delete", first).hide();
	} else {
		$(".delete", first).show();
	}
}

personPage.delete_email = function(){
	return personPage.delete_element($(this), "email");
}
personPage.delete_phone_number = function(){
	return personPage.delete_element($(this), "phone_number");	
}

personPage.detail_tab_clicked = function(e) {
    var tab_link = $(e.target);
    var tab_name = tab_link.attr("href");
    load_detail_tab(tab_name);   
    return false;
};

personPage.primary_clicked = function() {
	var ele = $(this);
	var can_containter = ele.parents(".canonical_set_container");
	$(".canonical", can_containter).removeClass("is_primary");
	ele.parents(".canonical").addClass("is_primary");
	$(".primary_field input:checked", can_containter).removeAttr("checked").trigger("change");
	$(".primary_field input", ele.parents(".primary")).attr("checked", "checked")
	$(".primary_field input", ele.parents(".primary")).trigger("change");

}

personPage.load_detail_tab = function(tab_name) {
    tab_link = $("detail_tabs a[href="+tab_name+"]");
    var tab_container = tab_link.parents("detail_tabs");
    if (tab_name != personPage.prev_tab_name) {
        // Switch the current tab
        personPage.prev_tab_name = tab_name;
        $("fragment[name=detail_tab]").html("Loading...");
        $(".detail_tab.current", tab_container).removeClass("current");
        tab_link.addClass("current");

        // Go get the tab content from the server.
        $.Mycelium.fragments.get_and_update_fragments(tab_container.attr("update_url"), {
            "data": {'tab_name': tab_name},
            "async": false
        });
        switch(tab_name){
        	
            case "#conversations":
                bind_conversation_tab_events();
                break;
            case "#volunteer":
                bind_volunteer_tab_events();
                break;
            case "#donor":
                bind_donor_tab_events();                
                break;
            case "#groups":
                bind_groups_tab_events();
                break;
            case "#tags":
            	bind_tags_tab_events();
            	break;
        }
        $.bbq.pushState({"current_detail_tab":tab_name})
    } 
};

personPage.delete_person = function(e) {
    var name = $("#container_id_first_name .view_field").text() + " " + $("#container_id_last_name .view_field").text();
    if (name == " ") {
        name = "Unnamed Person";
    }
    if (confirm("Are you sure you want to completely delete " + name + " from the database? \n\nDeleting will remove this person, all their data (contact info, job info, etc), AND all of their donations, all of the volunteer shifts, everything.\n\n  It cannot be undone.\n\nPress OK to delete "+ name +".\nPress Cancel to leave things unchanged.")) {
        $(window).unbind("unload.genericFieldForm");
        $("#delete_person_form").submit();
    }
};




// Handled by convention
// var person_form_options = {
// 		form_objects: {
// 			"person": {
// 				get_objects: function(){ 
// 					return $.fn.genericAjaxFormClasses().createPageObjectFromCanonical(this, ".person.canonical");
// 				},
// 				get_data: function(page_object){ 
// 					// Gets form input, select, etc data prior to ajax POST. 
// 					return $.fn.genericAjaxFormClasses.getFormFieldData(page_object.target)
// 				},
// 			},
// 			"phone_number": {
// 				get_objects: function(){
// 					return $.fn.genericAjaxFormClasses().createPageObjectFromCanonical(this, ".phone_number.canonical");
// 				},
// 				get_data: function(page_object){ 
// 					// Gets form input, select, etc data prior to ajax POST. 
// 					return $.fn.genericAjaxFormClasses.getFormFieldData(page_object.target)
// 				},
// 			},
// 			"email": {
// 				get_objects: function(){
// 					return $.fn.genericAjaxFormClasses().createPageObjectFromCanonical(this, ".email.canonical");
// 				},
// 				get_data: function(page_object){ 
// 					// Gets form input, select, etc data prior to ajax POST. 
// 					return $.fn.genericAjaxFormClasses.getFormFieldData(page_object.target)
// 				},
// 			},
// 			"employee": {
// 				get_objects: function(){
// 					return $.fn.genericAjaxFormClasses().createPageObjectFromCanonical(this, ".employee.canonical");
// 				},
// 				get_data: function(page_object){ 
// 					// Gets form input, select, etc data prior to ajax POST. 
// 					return $.fn.genericAjaxFormClasses.getFormFieldData(page_object.target)
// 				},
// 			}
// 		}
// 	}
