(function($){
    $(".people_volunteer_tab #new_completed_volunteer_shift input[name=duration]").live("change",volunteerTab.round_volunteer_shift);
    $(".people_volunteer_tab .year_details_link").live("click",volunteerTab.toggle_year_details);
    $(".people_volunteer_tab #new_completed_volunteer_shift .cancel_add_btn").live("click", volunteerTab.cancel_add_shift);
    $(".people_volunteer_tab .delete_shift_btn").live("click",volunteerTab.delete_completed_volunteer_from_people_tab);
    bind_volunteer_tab_events();
});

function process_fragments_and_rebind_volunteer_shift_form(json) {
        $.Mycelium.fragments.process_fragments_from_json(json);
        bind_volunteer_tab_events();
}

function bind_volunteer_tab_events() {
	$("#new_completed_volunteer_shift").ajaxForm({
        "success":process_fragments_and_rebind_volunteer_shift_form,
        "dataType": 'json'
    });
    $("#new_completed_volunteer_shift .sentence input").autoGrowInput({comfortZone: 20, resizeNow:true});
    $("#new_completed_volunteer_shift input[name=date]").datepicker({
        numberOfMonths: 2,
        showButtonPanel: true,
        // gotoCurrent: true
        showCurrentAtPos: 1            
    });
    $(".status_and_skills input[name$=reactivation_date]").datepicker();    
    $("tabbed_box[name=add_a_volunteer_shift]").bind("mycelium.tabbed_box.opened",function(){
        $("#new_completed_volunteer_shift input[name$=duration]").focus();
    });
    $("#volunteer_status_and_skills").genericFieldForm();
    $(".people_volunteer_tab .status_and_skills .skills_tags").genericTags({'mode':'checkbox'});
    $.Mycelium.update_stripes(".year_of_shifts");
    volunteerTab.show_or_hide_datefield();
    $(".status_and_skills input[name$=status]").change(volunteerTab.show_or_hide_datefield);
}

var volunteerTab = new Object();
volunteerTab.round_volunteer_shift = function() {
    input = $(this);
    dur = input.val();
    dur = Math.round(dur*4)/4;
    input.val(dur);
}
volunteerTab.toggle_year_details = function() {
    var link = $(this);
    if (link.text() == "See details") {
        link.html("Hide details");
    } else {
        link.html("See details");
    }
    link.parents(".year_overview").next(".year_of_shifts").toggle();
    return false;
}
volunteerTab.cancel_add_shift = function() {
    $("tabbed_box[name=add_a_volunteer_shift] tab_title").trigger("click");
    return false;
}

volunteerTab.show_or_hide_datefield = function(){
    if ($(".status_and_skills input[name$=status]:checked").val() == "temp_inactive") {
        $(".status_and_skills .reactivation_date").show();
    } else {
        $(".status_and_skills .reactivation_date").hide();
        $(".status_and_skills .generic_editable_field[id$=reactivation_date] input").val("");
    }
}

volunteerTab.delete_completed_volunteer_from_people_tab = function() {
	var row = $(this).parents(".completed_volunteer_shift_row");
	row.addClass("pre_delete");
	var confirm_response = confirm("Are you sure you want to remove this shift?\n\nPress OK to remove the shift.\nPress Cancel to leave things as-is.");
	if (confirm_response) {
		$.ajax({
			url: $(this).attr("href"),
			type: "GET",
			dataType: "json",
			success: function(json) {
			$.Mycelium.fragments.process_fragments_from_json(json);
            process_fragments_and_rebind_volunteer_shift_form(json);
			}
		});		
	} else {
		row.removeClass("pre_delete");		
	}
	
    return false;	
}