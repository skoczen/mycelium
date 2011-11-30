$(function(){
	personPage.init();
});

var personPage = {};
personPage.tag_fadeout_timeout = false;
personPage.prev_tab_name = "#recent_activity";

personPage.init = function() {
	personPage.create_blank_phone_number();
	
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

personPage.create_blank_phone_number = function() {
	$("#phone_number_form_container").append("<span class='phone_number_canonical_container blank'></span>");

	$(".phone_number_canonical_container.blank").html($("#phone_number_form_container .phone_number_canonical_container:first").html());
	$(".phone_number_canonical_container.blank .phone_number.canonical").attr("pk", "").attr("page_pk", "");
	$(".phone_number_canonical_container.blank .contact_type").html("");
	$(".phone_number_canonical_container.blank .primary").html("");
	$(".phone_number_canonical_container.blank .number input").val("").attr("placeholder", "Add a phone number");
	$(".phone_number_canonical_container.blank .number .view_field").html("");
	$(".phone_number_canonical_container.blank input, .phone_number_canonical_container.blank select").addClass("excluded_field");
	personPage.convert_zero_elements_to_blank($(".phone_number_canonical_container.blank .number input"));

	$(".phone_number_canonical_container.blank .number input").unbind("keyup");
	$(".phone_number_canonical_container.blank .number input").keyup(personPage.blank_phone_number_changed);	
}
personPage.convert_zero_elements_to_blank = function(ele) {
	$(ele).each(function(){
		var e = $(this);
		e.attr("name", e.attr("name").replace("-0-","-BLANK-"));
		e.attr("id", e.attr("id").replace("-0-","-BLANK-"));
		try {
			e.val("");
		} catch(e) {}
	});
}
personPage.convert_blank_elements_to_new = function(ele, counter) {
	$(ele).each(function(){
		var e = $(this);
		e.attr("name", e.attr("name").replace("-BLANK-", "-"+counter+"-"));
		e.attr("id", e.attr("id").replace("-BLANK-", "-"+counter+"-"));
	});
}
personPage.cloned_and_cleared = function(ele) {
	var e = ele.clone()
	try {
		$("select, input",e).val("");
	} catch(e) {}
	personPage.convert_zero_elements_to_blank($("select, input",e));
	return e.html();
}

personPage.blank_phone_number_changed = function() {
	var ele = $(this);
	if (ele.val() != "") {
		// Make a new one, initialize the fields.
		var num_phone_numbers = $("#phone_number_form_container .phone_number.canonical").length;
		$(".phone_number_canonical_container.blank .contact_type").html(personPage.cloned_and_cleared($("#phone_number_form_container .contact_type:first")));
		$(".phone_number_canonical_container.blank .primary").html(personPage.cloned_and_cleared($("#phone_number_form_container .primary:first")));

		personPage.convert_blank_elements_to_new($(".phone_number_canonical_container.blank select, .phone_number_canonical_container.blank input"), num_phone_numbers);
		$(".phone_number_canonical_container.blank input, .phone_number_canonical_container.blank select").removeClass("excluded_field");
		$(".phone_number_canonical_container.blank").removeClass("blank");
		$(".phone_number_canonical_container.blank .number input").unbind("keyup");

		personPage.create_blank_phone_number();
	}
	return false;
}

personPage.detail_tab_clicked = function(e) {
    var tab_link = $(e.target);
    var tab_name = tab_link.attr("href");
    load_detail_tab(tab_name);   
    return false;
};

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
