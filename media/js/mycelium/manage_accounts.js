$(function(){
    $("#basic_info_form").genericFieldForm();

    $.Mycelium.update_stripes();
	$("#new_account #container_id_first_name input").bind("change",populate_username);
	$("#new_account #container_id_first_name input").bind("keyup",populate_username);
	
	$("#new_account input[type=text]").autoGrowInput({comfortZone: 30, resizeNow:true});
	$("#new_account input").bind("change keyup blur",enable_disable_add_button);

	$("tabbed_box.with_button").bind("mycelium.tabbed_box.opened",box_opened);
	$(".cancel_add_btn").click(cancel_add_account);
	$(".reset_password_btn").click(reset_password_clicked);
	$(".delete_user_btn").click(delete_user_clicked);

	$(".change_password_btn").click(show_change_password_field);
	$("#save_new_password_btn").click(save_new_password);
	$("#cancel_new_password_btn").click(cancel_new_password);
	$(".cancel_subscription_btn").click(confirm_cancel_subscription);

	$("a.billing_popup_link").colorbox({
		'iframe':true,
		'width':"75%",
		'height':"85%",
		'onClosed': force_reload_page,
	});
	$(".close_overlay_link").click(close_colorbox)

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

function reset_password_clicked() {
	row = $(this).parents("tr");
	if ( confirm("Are you sure you want to reset the password for " + $(".full_name",row).html() + "?\n\nClick OK to reset their password.\nClick Cancel to leave it unchanged.\n") ) {
			$.ajax({
             url: $(this).attr("href"),
             type: "GET",
             dataType: "json",
             success: function(json) {
                alert("The password for " + $(".full_name",row).html() + " has been reset to 'changeme!'\n\nPlease do change it :)" );
             }
           });	
	}
	return false;
}
function delete_user_clicked () {
	row = $(this).parents("tr");
	row.addClass("pre_delete")
	delete_it = confirm("Are you sure you want to delete the account for " + $(".full_name",row).html() + "?\n\nThis is permanent, but will not affect any data besides their account.\n\nClick OK to delete the account.\nClick Cancel to leave it alone.\n");
	if (!delete_it) {
		row.removeClass("pre_delete");
	}
	return delete_it
	
}

function show_change_password_field() {
	$(".password_saved_message").html("")
	$(".password_spacer").hide();
	$(".change_password_btn").hide();
	$(".new_password_field").removeClass("hidden").show();
	$("#id_new_password").focus();
}
function save_new_password(){
	var new_pass = $("#id_new_password").val();
	$.ajax({
		url: $("#id_new_password").attr("password_change_url"),
		type: "POST",
		dataType: "json",
		data: {'new_password':new_pass},
		mode: 'abort',
		success: function(json) {
			cancel_new_password();
			$(".password_saved_message").html("New password saved.");
		}
     });
}
function cancel_new_password() {
	$(".new_password_field").hide();
	$("#id_new_password").val("");
	$(".password_spacer").show();
	$(".change_password_btn").show();
}

function confirm_cancel_subscription() {
	return confirm("Are you sure you want to cancel your GoodCloud subscription?  This will take effect immediately.")
}

function force_reload_page() {
	window.location = $.param.querystring( window.location+"", "?force_reload=true");
}
function close_colorbox() {
	parent.jQuery.colorbox.close();
}