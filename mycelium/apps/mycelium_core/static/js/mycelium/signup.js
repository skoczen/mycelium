$(function(){
	$("#signup_form input").autoGrowInput({'comfortZone': 30, 'resizeNow':true});	
	$("#signup_form input").bind("change keyup blur",enable_disable_signup_button);

	$("#container_id_name input").focus();
	$("#container_id_name input").bind("change",populate_subdomain);
	$("#container_id_name input").bind("keyup",populate_subdomain);
	$("#container_id_subdomain input").bind("focus",subdomain_focused);
	$(".form_section.you input").bind("focus",bottom_field_focused);
	$("#container_id_subdomain input").bind("change keyup",subdomain_changed);
	
	$("#container_id_first_name input").bind("change",populate_username);
	$("#container_id_first_name input").bind("keyup",populate_username);
	$("#container_id_username input").bind("focus",username_focused);

	enable_disable_signup_button();
});

var subdomain_has_been_focused = false;
var username_has_been_focused = false;
var bottom_field_has_been_focused = false;
function populate_subdomain() {
	var subdomain = $("#container_id_subdomain input");
	if (!subdomain_has_been_focused) {
		var name = $("#container_id_name input").val().replace(/[^a-zA-Z0-9-]+/g,'');
		subdomain.val($.trim(name).toLowerCase());
		subdomain.autoGrowInput({comfortZone: 30, resizeNow:true});
	}
}

function populate_username() {
	var username = $("#container_id_username input");
	if (!username_has_been_focused) {
		var name = $("#container_id_first_name input").val();
		var index = name.indexOf(" ");
		if (index > 0) {
			name = name.substring(0,index);
		}
		username.val($.trim(name).toLowerCase());
	}
}

function subdomain_focused() {
	subdomain_has_been_focused = true;
}
function username_focused() {
	username_has_been_focused = true;
}
function bottom_field_focused() {
	if (!bottom_field_has_been_focused && $("#subdomain_verification").hasClass("not_verified")) {
		if ($("#container_id_subdomain input").val() != "") {
			verify_subdomain();
			bottom_field_has_been_focused = true;
		}
	}
}

function form_is_valid() {
	var missing_val = false; 
	$("#signup_form input").each(function(){
		if ($(this).val() == "") {
			missing_val = true;
		}
	});
	if ($("#subdomain_verification").hasClass("not_verified")) {
		missing_val = true;
	}
	if ($("#id_agreed_to_terms:checked").length == 0) {
		missing_val = true;
	}
	return !missing_val;
}
function enable_disable_signup_button() {
	if (form_is_valid()) {
		$("#submit_button").removeAttr("disabled").removeClass("disabled");
	} else {
		$("#submit_button").attr("disabled", "disabled").addClass("disabled");
	}
}
var old_subdomain_value = "aksdljfli3";
var verify_timeout = false;
function subdomain_changed() {
	if ($("#container_id_subdomain input").val() != old_subdomain_value) {
		$("#container_id_subdomain input").val($.trim($("#container_id_subdomain input").val().replace(/[^a-zA-Z0-9-]+/g,'')).toLowerCase());
		$("#subdomain_verification").addClass("not_verified");
		clearTimeout(verify_timeout);
		verify_timeout = setTimeout(verify_subdomain, 500);
	}
}
var verifying_message_timeout = false;
function verify_subdomain() {
	$("#subdomain_verification").show();
	var requested_subdomain = $("#container_id_subdomain input").val();
	var subdomain_message = $("#subdomain_verification .subdomain_response");

	if (requested_subdomain != "") {
		clearTimeout(verifying_message_timeout);
		verifying_message_timeout = setTimeout(function(){
			subdomain_message.html("Checking availability for <br/> " + requested_subdomain + ".agoodcloud.com").addClass("pending").removeClass("verified").removeClass("trouble");;
		}, 300);
		$.ajax({
			url: $("#subdomain_verification").attr("verification_url"),
			type: "POST",
			dataType: "json",
			data: {'subdomain':requested_subdomain},
			mode: 'abort',
			success: function(json) {
				clearTimeout(verifying_message_timeout);
				old_subdomain_value = $("#container_id_subdomain input").val();
				if (json.is_available) {
					subdomain_message.removeClass("trouble").removeClass("pending").addClass("verified").html("Looks good! <span class='domain'>" + requested_subdomain + ".agoodcloud.com</span> is all yours.");
					$("#subdomain_verification").removeClass("not_verified");
					enable_disable_signup_button();
				} else {
					subdomain_message.addClass("trouble").removeClass("pending").html("Sorry, " + requested_subdomain + ".agoodcloud.com is already taken.<br/> Please try another name!");
				}
			}
	     });
	} else {
		subdomain_message.html("");
	}
}