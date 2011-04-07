$(function(){
	$("rule left_side select").live("change",left_side_changed);
});

function left_side_changed() {
	var left_select = $(this);
	var rule = left_select.parents("rule");
	var left_side_logic = RULES_LOGIC.left_sides[left_select.val()]

	// set operators
	var operator_html = "";
	for (var j=0; j<left_side_logic.operator_ids.length; j++) {
		operator_html += RULES_LOGIC.operators[left_side_logic.operator_ids[j]].partial;
	};
	$("operator select",rule).html(operator_html)

	// set right side
	$("right_side .edit_field",rule).html(left_side_logic.right_side_partial)
	


}