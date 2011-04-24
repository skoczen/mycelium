$(function(){
	$("#signup_form input").autoGrowInput({comfortZone: 30, resizeNow:true});
	$("#signup_form input").bind("change keyup blur",enable_disable_signup_button);

	$("#container_id_name input").focus();
	$("#container_id_name input").bind("change",populate_subdomain);
	$("#container_id_name input").bind("keyup",populate_subdomain);
	$("#container_id_subdomain input").focus(subdomain_focused);
	$("#container_id_subdomain input").bind("change keyup",subdomain_changed);
	
	$("#container_id_first_name input").bind("change",populate_username);
	$("#container_id_first_name input").bind("keyup",populate_username);
	$("#container_id_username input").focus(username_focused);
	enable_disable_signup_button();
});

subdomain_has_been_focused = false;
username_has_been_focused = false;
function populate_subdomain() {
	subdomain = $("#container_id_subdomain input");
	if (!subdomain_has_been_focused) {
		name = $("#container_id_name input").val().replace(/[^a-zA-Z0-9-]+/g,'');
		subdomain.val($.trim(name).toLowerCase());
		subdomain.autoGrowInput({comfortZone: 30, resizeNow:true});
	}
}

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

function subdomain_focused() {
	subdomain_has_been_focused = true;
}
function username_focused() {
	username_has_been_focused = true;
}

function form_is_valid() {
	missing_val = false; 
	$("#signup_form input").each(function(){
		if ($(this).val() == "") {
			missing_val = true;
		}
	});
	if ($("#subdomain_verification").hasClass("not_verified")) {
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
old_subdomain_value = "aksdljfli3";
verify_timeout = false;
function subdomain_changed() {
	if ($("#container_id_subdomain input").val() != old_subdomain_value) {
		$("#container_id_subdomain input").val($.trim($("#container_id_subdomain input").val().replace(/[^a-zA-Z0-9-]+/g,'')).toLowerCase());
		$("#subdomain_verification").addClass("not_verified");
		clearTimeout(verify_timeout)
		verify_timeout = setTimeout(verify_subdomain, 500);		
	}

}
function verify_subdomain() {
	requested_subdomain = $("#container_id_subdomain input").val();
	subdomain_message = $("#subdomain_verification .subdomain_response");

	if (requested_subdomain != "") {
		subdomain_message.html("Checking availability for <br/> " + requested_subdomain + ".agoodcloud.com").addClass("pending").removeClass("verified").removeClass("trouble");
	} else {
		subdomain_message.html("");
	}
	$.ajax({
		url: $("#subdomain_verification").attr("verification_url"),
		type: "POST",
		dataType: "json",
		data: {'subdomain':requested_subdomain},
		mode: 'abort',
		success: function(json) {
			old_subdomain_value = $("#container_id_subdomain input").val();
			if (json.is_available) {
				subdomain_message.removeClass("trouble").removeClass("pending").addClass("verified").html("Looks good! " + requested_subdomain + ".agoodcloud.com is all yours.");
				$("#subdomain_verification").removeClass("not_verified");
				enable_disable_signup_button();
			} else {
				subdomain_message.addClass("trouble").removeClass("pending").html("Sorry, " + requested_subdomain + ".agoodcloud.com is already taken.<br/> Please try another name!");
			}
		}
     });	
}