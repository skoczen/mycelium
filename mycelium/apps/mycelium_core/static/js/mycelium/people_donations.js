$(function(){
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
donorTab.toggle_notes = function() {
	var row = $(this).parents(".donation_row");
	$(".notes_body",row).toggle();
}

donorTab.honorarium_checkbox_clicked = function() {
	var me = $(this);
	var hon = $("#id_in_honor_of");
	var mem = $("#id_in_memory_of");
	var hon_checked = $("#id_in_honor_of:checked");
	var mem_checked = $("#id_in_memory_of:checked");

	if (me.attr("id") == hon.attr("id")) {
		if (hon_checked.length) {
			$(".in_honor_of").addClass("checked");
			mem.removeAttr("checked");
			$(".in_memory_of").removeClass("checked");
		} else {
			$(".in_honor_of").removeClass("checked");
		}
	} else {
		if (mem_checked.length) {
			$(".in_memory_of").addClass("checked");
			hon.removeAttr("checked");
			$(".in_honor_of").removeClass("checked");
		} else {
			$(".in_memory_of").removeClass("checked");
			$(".in_honor_of").removeClass("checked");
		}
	}

	hon_checked = $("#id_in_honor_of:checked");
	mem_checked = $("#id_in_memory_of:checked");
	if (hon_checked.length) {
		if ( $(".people_donor_tab .in_honor_of .honorarium_name").length == 0) {
			$(".people_donor_tab #new_donation .in_honor_of").append(donorTab.honorarium_html)
			$(".people_donor_tab #new_donation .in_honor_of .honorarium_name_fragment input").focus();
		}
		$(".people_donor_tab #new_donation .in_memory_of .honorarium_name").remove();
	} else {
		if (mem_checked.length) {
			console.log($(".people_donor_tab .in_memory_of .honorarium_name").length);
			if ($(".people_donor_tab .in_memory_of .honorarium_name").length == 0) {
				$(".people_donor_tab #new_donation .in_memory_of").append(donorTab.honorarium_html);
				$(".people_donor_tab #new_donation .in_memory_of .honorarium_name_fragment input").focus();
			}
			$(".people_donor_tab #new_donation .in_honor_of .honorarium_name").remove();
			console.log("removed");
		} else {
			$(".people_donor_tab #new_donation .in_memory_of .honorarium_name").remove();
			$(".people_donor_tab #new_donation .in_honor_of .honorarium_name").remove();
		}
	}
		

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
    $(".people_donor_tab .notes_icon").click(donorTab.toggle_notes);
    $(".people_donor_tab #new_donation #id_notes").autogrow();
    $(".people_donor_tab #new_donation .honorarium input:checkbox").change(donorTab.honorarium_checkbox_clicked);
    donorTab.honorarium_html = $(".honorarium_fragment").html();
	$(".honorarium_fragment").html("").remove();
}

function process_fragments_and_rebind_donation_form(json) {
        $.Mycelium.fragments.process_fragments_from_json(json);
        bind_donor_tab_events();
}
