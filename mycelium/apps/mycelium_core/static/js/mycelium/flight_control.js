$(function(){
	$(".delete_account_link").click(delete_account_link_clicked);
	$(".reset_password").click(reset_password_clicked);
});

function delete_account_link_clicked() {
	return confirm("Are you certain you want to permanently delete this account?\n\nThere's no going back. \n\nHit OK to delete the account.\nHit Cancel to leave it in GoodCloud.");
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