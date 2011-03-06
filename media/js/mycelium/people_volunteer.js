$(function(){
    $("#new_completed_volunteer_shift input[name=duration]").live("change",round_volunteer_shift);
    $(".year_details_link").live("click",toggle_year_details);
    $("#new_completed_volunteer_shift .cancel_add_btn").live("click", cancel_add_shift);
    $(".delete_shift_btn").live("click",delete_completed_volunteer_from_people_tab);
});

function round_volunteer_shift() {
    input = $(this);
    dur = input.val();
    dur = Math.round(dur*4)/4
    input.val(dur);
}
function toggle_year_details() {
    var link = $(this)
    if (link.text() == "See details") {
        link.html("Hide details");
    } else {
        link.html("See details");
    }
    link.parents(".year_overview").next(".year_of_shifts").toggle();
    return false;
}
function cancel_add_shift() {
    $("tabbed_box[name=add_a_volunteer_shift] tab_title").trigger("click");
    return false;
}

function process_fragments_and_rebind_volunteer_shift_form(json) {
        $.Mycelium.fragments.process_fragments_from_json(json);
        $("#new_completed_volunteer_shift").ajaxForm({
            "success":process_fragments_and_rebind_volunteer_shift_form,
            "dataType": 'json'
        });
        $("#new_completed_volunteer_shift .sentence input").autoGrowInput({comfortZone: 20, resizeNow:true});
        $("#new_completed_volunteer_shift input[name$=date]").datepicker({
            numberOfMonths: 2,
            showButtonPanel: true,
            // gotoCurrent: true
            showCurrentAtPos: 1                
        });
        $("tabbed_box[name=add_a_volunteer_shift]").bind("mycelium.tabbed_box.opened",function(){
            $("#new_completed_volunteer_shift input[name$=duration]").focus()
        });
        $.Mycelium.update_stripes(".year_of_shifts");
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
    $("tabbed_box[name=add_a_volunteer_shift]").bind("mycelium.tabbed_box.opened",function(){
        $("#new_completed_volunteer_shift input[name$=duration]").focus()
    });
    $.Mycelium.update_stripes(".year_of_shifts");
}

function delete_completed_volunteer_from_people_tab() {
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
			},
		});		
	} else {
		row.removeClass("pre_delete");		
	}
	
    return false;	
}