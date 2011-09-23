$(function(){
	$(".delete_account_link").click(delete_account_link_clicked);
});

function delete_account_link_clicked() {
	return confirm("Are you certain you want to permanently delete this account?\n\nThere's no going back. \n\nHit OK to delete the account.\nHit Cancel to leave it in GoodCloud.");
}