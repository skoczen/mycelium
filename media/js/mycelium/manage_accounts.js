$(function(){
    $("#basic_info_form").genericFieldForm();
    $.Mycelium.update_stripes();
	$("#new_account #container_id_first_name input").bind("change",populate_username);
	$("#new_account #container_id_first_name input").bind("keyup",populate_username);
	
	$("#new_account input[type=text]").autoGrowInput({comfortZone: 30, resizeNow:true});
	$("#new_account input").bind("change keyup blur",enable_disable_add_button);

	$("tabbed_box.with_button").bind("mycelium.tabbed_box.opened",box_opened);
	$(".cancel_add_btn").click(cancel_add_account);
});

username_has_been_focused = false;
function populate_username() {
	username = $("#container_id_username input");
	if (!username_has_been_focused) {
		name = $("#container_id_first_name input").val();
		index = name.indexOf(" ");
		if (index > 0) {
			name = name.substring(0,index)
		}
		username.val($.trim(name).toLowerCase());
	}
}
function box_opened() {
	$("#new_account #container_id_first_name input").focus();
	enable_disable_add_button();
}
function form_is_valid() {
	console.log("checking form..")
	var is_valid = true;
	$("#new_account input[type=text]").each(function(){
		i = $(this);
		if (i.val() == "") {
			is_valid = false;
		}
	});
	if ($("#new_account input[type=radio]:checked").length == 0 ) {
		is_valid = false;
	}
	console.log(is_valid)
	return is_valid;
}

function enable_disable_add_button() {
	if (form_is_valid()) {
		$(".create_account_btn").removeAttr("disabled").removeClass("disabled");
		$(".all_fields_message").hide();
	} else {
		$(".create_account_btn").attr("disabled", "disabled").addClass("disabled");
		$(".all_fields_message").show();
	}
}
function cancel_add_account(){
	$("tabbed_box tab_title").trigger("click");
}