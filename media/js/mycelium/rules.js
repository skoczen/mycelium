(function($){
	$("rule left_side select").live("change",left_side_changed);
	$("rule left_side select").each(left_side_changed);
});

function left_side_changed() {
	var left_select = $(this);
	var rule = left_select.parents("rule");
	if (left_select.val() != "") {
		var left_side_logic = RULES_LOGIC.left_sides[left_select.val()]

		// set operators
		operator_field = $("operator select",rule);
		var old_operator_val = operator_field.val()
		var operator_html = "";
		for (var j=0; j<left_side_logic.operator_ids.length; j++) {
			operator_html += RULES_LOGIC.operators[left_side_logic.operator_ids[j]].partial;
		};
		operator_field.html(operator_html)
		try {
			operator_field.val(old_operator_val);
		}
		catch (e) {}

		// get right side meta
		var old_target;
		if ($("right_side .edit_field select",rule).length > 0) {
			old_target = $("right_side .edit_field select",rule);
		} else {
			if ($("right_side .edit_field input",rule).length > 0) {
				old_target = $("right_side .edit_field input",rule);
			} else {
				if ($("right_side .edit_field textarea",rule).length > 0) {
					old_target = $("right_side .edit_field textarea",rule);
				}
			}
		}
		var old_name = old_target.attr("name");
		var old_id = old_target.attr("id");
		var old_val = old_target.val()

		// set right side
		$("right_side .edit_field",rule).html(left_side_logic.right_side_partial)
		
		var new_target;
		if ($("right_side .edit_field select",rule).length > 0) {
			new_target = $("right_side .edit_field select",rule);
		} else {
			if ($("right_side .edit_field input",rule).length > 0) {
				new_target = $("right_side .edit_field input",rule);
			} else {
				if ($("right_side .edit_field textarea",rule).length > 0) {
					new_target = $("right_side .edit_field textarea",rule);
				}
			}
		}
		new_target.attr("name",old_name);
		new_target.attr("id",old_id);		
		
		// if it's a date, add a datepicker
		if (left_side_logic.is_date) {
			new_target.datepicker({
		        "numberOfMonths": 2,
		        "showButtonPanel": true,
		        // "gotoCurrent": true,
		        "showCurrentAtPos": 1            
		    });    
		}
		

		// set right side type
		$("input[name$=right_side_type]",rule).val(left_side_logic.right_side_type)

		// try to keep the value
		try {
			new_target.val(old_val);
		} 
		catch (e) {}
	}
	

}