(function($){
    $(".people_donor_tab #new_donation input[name=amount]").live("change",donorTab.round_donation);
    $(".people_donor_tab .year_details_link").live("click",donorTab.toggle_year_details);
    $(".people_donor_tab #new_donation .cancel_add_btn").live("click", donorTab.cancel_add_donation);
    $(".people_donor_tab .delete_donation_btn").live("click",donorTab.delete_donor_from_people_tab);

});


var donorTab = new Object();
donorTab.round_donation = function() {
    input = $(this);
    dur = parseFloat(input.val()).toFixed(2);
    input.val(dur);
}
donorTab.toggle_year_details = function() {
    var link = $(this);
    if (link.text() == "See details") {
        link.html("Hide details");
    } else {
        link.html("See details");
    }
    link.parents(".year_overview").next(".year_of_donations").toggle();
    return false;
}
donorTab.cancel_add_donation = function() {
    $("tabbed_box[name=add_a_donation] tab_title").trigger("click");
    return false;
}



donorTab.delete_donor_from_people_tab = function() {
	var row = $(this).parents(".donation_row");
	row.addClass("pre_delete");
	var confirm_response = confirm("Are you sure you want to remove this donation?\n\nPress OK to remove the donation.\nPress Cancel to leave things as-is.");
	if (confirm_response) {
		$.ajax({
			url: $(this).attr("href"),
			type: "GET",
			dataType: "json",
			success: function(json) {
			$.Mycelium.fragments.process_fragments_from_json(json);
            process_fragments_and_rebind_donation_form(json);
			}
		});		
	} else {
		row.removeClass("pre_delete");		
	}
	
    return false;	
}

function bind_donor_tab_events() {
    $("#new_donation").ajaxForm({
        "success":process_fragments_and_rebind_donation_form,
        "dataType": 'json'
    });
    $("#new_donation .sentence input").autoGrowInput({comfortZone: 20, resizeNow:true});
    $("tabbed_box[name=add_a_donation]").bind("mycelium.tabbed_box.opened",function(){
        $("#new_donation input[name$=amount]").focus();
    });
    $.Mycelium.update_stripes(".year_of_donations");
    $(".people_donor_tab .tags_and_other_info").genericTags();
    $("#new_donation input[name=date]").datepicker({
        "numberOfMonths": 2,
        "showButtonPanel": true,
        // "gotoCurrent": true,
        "showCurrentAtPos": 1            
    });    
}

function process_fragments_and_rebind_donation_form(json) {
        $.Mycelium.fragments.process_fragments_from_json(json);
        bind_donor_tab_events();
}
