# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from organizations.tests.selenium_abstractions import OrganizationsTestAbstractions
from groups.tests.selenium_abstractions import GroupTestAbstractions
from django.conf import settings
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from django.core.cache import cache
    
class TestAgainstLiterallyNoData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, OrganizationsTestAbstractions, AccountTestAbstractions, GroupTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.a1 = self.setup_for_logged_in_with_no_data()
        cache.clear()
        self.verificationErrors = []

    def test_setting_access_levels_for_a_user_stays(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_the_manage_accounts_page()

        # make everyone else admins
        assert not sel.is_element_present("css=.user_row:nth(2) .access_level label:nth(0) input:checked")
        assert not sel.is_element_present("css=.user_row:nth(3) .access_level label:nth(0) input:checked")
        sel.click("css=.user_row:nth(2) .access_level input:nth(0)")
        sel.click("css=.user_row:nth(3) .access_level input:nth(0)")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_element_present("css=.user_row:nth(2) .access_level label:nth(0) input:checked")
        assert sel.is_element_present("css=.user_row:nth(3) .access_level label:nth(0) input:checked")

        # make everyone else staff
        assert not sel.is_element_present("css=.user_row:nth(2) .access_level label:nth(1) input:checked")
        assert not sel.is_element_present("css=.user_row:nth(3) .access_level label:nth(1) input:checked")
        sel.click("css=.user_row:nth(2) .access_level input:nth(1)")
        sel.click("css=.user_row:nth(3) .access_level input:nth(1)")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_element_present("css=.user_row:nth(2) .access_level label:nth(1) input:checked")
        assert sel.is_element_present("css=.user_row:nth(3) .access_level label:nth(1) input:checked")

        # make everyone else a volunteer
        assert not sel.is_element_present("css=.user_row:nth(2) .access_level label:nth(2) input:checked")
        assert not sel.is_element_present("css=.user_row:nth(3) .access_level label:nth(2) input:checked")
        sel.click("css=.user_row:nth(2) .access_level input:nth(2)")
        sel.click("css=.user_row:nth(3) .access_level input:nth(2)")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_element_present("css=.user_row:nth(2) .access_level label:nth(2) input:checked")
        assert sel.is_element_present("css=.user_row:nth(3) .access_level label:nth(2) input:checked")


class TestAgainstNoData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, OrganizationsTestAbstractions, AccountTestAbstractions, GroupTestAbstractions):
    # selenium_fixtures = []
    # # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()
        cache.clear()
        self.verificationErrors = []

    def test_that_logging_in_works(self):
        self.go_to_the_login_page()
        self.log_in()
        self.assert_login_succeeded()

    def test_that_and_invalid_username_and_password_errors_helpfully(self):
        sel = self.selenium
        self.go_to_the_login_page()
        sel.type("css=input[name=username]","asfjkaskjldf")
        sel.type("css=input[name=password]","21k3jlkjdsf")
        sel.click("css=.login_btn")
        sel.wait_for_page_to_load("30000")
        self.assert_login_failed()

    def test_that_opening_the_people_page_without_logging_in_returns_to_the_login_page(self):
        sel = self.selenium
        self.go_to_the_login_page()
        self.open("/people")
        assert sel.is_element_present("css=.login_btn")

    def test_that_site2s_user_cannot_log_into_site_one(self):
        
        a2 = self.create_demo_site("test2")
        self.go_to_the_login_page()
        ua = Factory.useraccount(account=a2)
        self.log_in(ua=ua, with_assert=False)
        self.assert_login_failed()

        self.go_to_the_login_page("test2")
        self.log_in(ua=ua)
        self.assert_login_succeeded()

    def test_that_logged_in_site2s_user_cannot_manually_browse_to_site_ones_page(self):
        sel = self.selenium
        a2 = self.create_demo_site("test2")
        ua = Factory.useraccount(account=a2)
        self.go_to_the_login_page("test2")
        self.log_in(ua=ua)
        self.assert_login_succeeded()

        self.go_to_the_login_page()
        self.open("/people")
        assert sel.is_element_present("css=.login_btn")


    def test_that_a_new_person_in_account_1_does_not_show_in_account_2(self):
        sel = self.selenium
        self.go_to_the_login_page()
        self.log_in()
        self.assert_login_succeeded()
        self.create_john_smith_and_verify()

        a2 = self.create_demo_site("test2")
        ua = Factory.useraccount(account=a2)
        cache.clear()
        self.go_to_the_login_page("test2")
        self.log_in(ua=ua)

        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "joh smith 555")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")

        time.sleep(2)
        assert not sel.is_text_present("John Smith")


    def test_that_a_new_person_in_account_1_does_not_show_in_account_2_org_people_search(self):
        sel = self.selenium
        self.go_to_the_login_page()
        self.log_in()
        self.assert_login_succeeded()
        self.create_john_smith_and_verify()
        self.create_new_organization()
        sel.click("css=tabbed_box tab_title")
        time.sleep(0.5)
        sel.click("id_search_new_person")
        sel.type("id_search_new_person", "john")
        time.sleep(2)
        assert sel.is_text_present('John Smith')
        

        a2 = self.create_demo_site("test2")
        ua = Factory.useraccount(account=a2)
        self.set_site("test2")
        self.go_to_the_login_page("test2")
        self.log_in(ua=ua)
        self.assert_login_succeeded()        
        
        self.create_new_organization()
        sel.click("css=tabbed_box tab_title")
        time.sleep(0.5)
        sel.click("id_search_new_person")
        sel.type("id_search_new_person", "john")
        time.sleep(2)
        assert sel.is_text_present('No people found for search "john".')

    def test_that_requesting_an_invalid_person_404s(self):
        sel = self.selenium
        self.go_to_the_login_page()
        self.log_in()
        self.assert_login_succeeded()
        # make sure to make a new person
        for i in range(0,20):
            Factory.person(account=self.a1)
        self.create_john_smith_and_verify()
        # get pk
        url = sel.get_location()
        person_url = url[url.find(":%s/" % settings.LIVE_SERVER_PORT)+5:]


        a2 = self.create_demo_site("test2")
        ua = Factory.useraccount(account=a2)
        self.go_to_the_login_page(site="test2")
        self.log_in(ua=ua)
        self.open(person_url, site="test2")
        assert sel.is_text_present("not found")
    
    def test_that_requesting_an_invalid_organization_404s(self):
        sel = self.selenium
        self.go_to_the_login_page()
        self.log_in()
        self.assert_login_succeeded()
        # make sure to make a new person
        for i in range(0,5):
            Factory.organization(account=self.a1)
        self.create_new_organization()
        # get pk
        url = sel.get_location()
        url = url[url.find(":%s/" % settings.LIVE_SERVER_PORT)+5:]


        a2 = self.create_demo_site("test2")
        ua = Factory.useraccount(account=a2)
        self.go_to_the_login_page(site="test2")
        self.log_in(ua=ua)
        self.open(url, site="test2")
        assert sel.is_text_present("not found")

    def test_that_requesting_an_invalid_group_404s(self):
        sel = self.selenium
        self.go_to_the_login_page()
        self.log_in()
        self.assert_login_succeeded()
        # make sure to make a new person
        for i in range(0,10):
            Factory.group(account=self.a1)
        self.create_new_group()
        # get pk
        url = sel.get_location()
        url = url[url.find(":%s/" % settings.LIVE_SERVER_PORT)+5:]

        a2 = self.create_demo_site("test2")
        ua = Factory.useraccount(account=a2)
        self.go_to_the_login_page(site="test2")
        self.log_in(ua=ua)
        self.open(url, site="test2")
        time.sleep(30)
        assert sel.is_text_present("not found")

    def test_that_logging_in_takes_you_to_the_dashboard(self):
        sel = self.selenium
        self.go_to_the_login_page()
        self.log_in()
        self.assert_login_succeeded()
        assert sel.is_element_present("css=salutation")

    def test_that_logging_in_after_trying_to_reach_a_specific_page_takes_you_to_that_page(self):
        sel = self.selenium
        # self.go_to_the_login_page()
        self.open("/more")
        self.log_in()
        self.assert_login_succeeded()
        assert sel.is_text_present("Update billing and account information")

    def test_that_the_account_signup_page_loads(self):
        sel = self.selenium
        sel.open("/signup")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("About your nonprofit")

    def test_that_valid_account_signup_works(self):
        sel = self.selenium
        self.test_that_the_account_signup_page_loads()
        sel.type("css=#id_name","My Test Organization")
        sel.type("css=#id_subdomain","test2")
        sel.focus("css=#id_subdomain")

        sel.type("css=#id_first_name","Joe Tester")
        sel.type("css=#id_email", "joe@example.com")
        sel.type("css=#id_username", "joe")
        sel.type("css=#id_password", "password")
        sel.click("css=#id_agreed_to_terms")
        time.sleep(2)

        sel.click("css=#submit_button")
        sel.wait_for_page_to_load("30000")
        self.go_to_the_login_page(site="test2")
        self.log_in(username="joe", password="password")

    
    def test_autofill_on_the_signup_page(self):
        sel = self.selenium
        self.test_that_the_account_signup_page_loads()

        # Basic check
        sel.type("css=#id_name","My Test Organization")
        sel.type("css=#id_first_name","Joe Tester")
        time.sleep(1)
        self.assertEqual(sel.get_value("css=#id_subdomain"),"mytestorganization")
        self.assertEqual(sel.get_value("css=#id_username"), "joe")

        # Make sure they keep updating
        sel.type("css=#id_name","Another Great Org")
        sel.type("css=#id_first_name","Tester Joe")
        time.sleep(1)
        self.assertEqual(sel.get_value("css=#id_subdomain"),"anothergreatorg")
        self.assertEqual(sel.get_value("css=#id_username"), "tester")

        # Manually changing one of the fields make them stop autofilling
        sel.type("css=#id_subdomain","test3")
        sel.type("css=#id_username", "william")
        sel.type("css=#id_name","My Test Organization")
        sel.type("css=#id_first_name","Joe Tester")
        time.sleep(1)
        self.assertEqual(sel.get_value("css=#id_subdomain"),"test3")
        self.assertEqual(sel.get_value("css=#id_username"), "william")



    def test_subdomain_verification(self):
        sel = self.selenium
        self.test_that_valid_account_signup_works()
        self.test_that_the_account_signup_page_loads()
        sel.type("css=#id_subdomain","test2")
        sel.focus("css=#id_subdomain")
        time.sleep(2)
        assert sel.is_text_present("Sorry,")

        sel.type("css=#id_subdomain","test20")
        sel.focus("css=#id_subdomain")
        time.sleep(2)
        assert sel.is_text_present("Looks good!")

    def test_how_tom_broke_signup_is_fixed(self):
        sel = self.selenium

        from django.contrib.auth.models import User
        User.objects.create_user("tom", "tom@agoodcloud.com", "Test123")

        self.test_that_the_account_signup_page_loads()
        sel.click("css=#id_name")
        sel.type("css=#id_name","Tom's Nonprofit")

        sel.click("css=#id_first_name")
        sel.type("css=#id_first_name","Tom Noble")
        sel.click("css=#id_email")
        sel.type("css=#id_email", "tom@agoodcloud.com")
        sel.click("css=#id_password")
        sel.type("css=#id_password", "Test123")
        sel.click("css=#id_agreed_to_terms")
        time.sleep(2)

        sel.click("css=#submit_button")
        sel.wait_for_page_to_load("30000")
        assert not sel.is_element_present("css=#submit_button")
        self.go_to_the_login_page(site="tomsnonprofit")
        self.log_in(username="tom", password="Test123")

    def test_creating_a_new_user(self, full_name="Joe Smith", username="jsmith", password="test"):
        self.setup_for_logged_in()
        self.create_a_new_user_via_manage_accounts()



    def test_resetting_a_password_changes_it_appropriately(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.create_a_new_user_via_manage_accounts()
        assert sel.is_element_present("css=.user_row:nth(4)")
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.user_row:nth(2) .reset_password_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to reset the password for Joe Smith?\n\nClick OK to reset their password.\nClick Cancel to leave it unchanged.\n")
        sel.click("css=.user_row:nth(2) .reset_password_btn")
        sel.get_confirmation()
        time.sleep(2)
        assert sel.is_alert_present()
        self.assertEqual(sel.get_alert(), "The password for Joe Smith has been reset to 'changeme!'  Please do change it :)")
        sel.click("css=.logout_btn")
        sel.wait_for_page_to_load("30000")
        sel.click("link=log back in")
        self.log_in(username="jsmith", password="changeme!")


    def test_that_deleting_your_account_logs_you_out_immediately(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_the_manage_accounts_page()
        sel.click("css=.user_row:nth(1) .delete_user_btn")
        sel.get_confirmation()
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Welcome to GoodCloud")
        # TODO: Intermittent fail because of random account ordering - need to actually make sure it's my account I'm deleting.

    def test_deleting_a_user(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.create_a_new_user_via_manage_accounts()
        assert sel.is_element_present("css=.user_row:nth(4)")
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.user_row:nth(2) .delete_user_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to delete the account for Joe Smith?\n\nThis is permanent, but will not affect any data besides their account.\n\nClick OK to delete the account.\nClick Cancel to leave it alone.\n")
        sel.click("css=.user_row:nth(2) .delete_user_btn")
        sel.get_confirmation()
        sel.wait_for_page_to_load("30000")
        assert not sel.is_element_present("css=.user_row:nth(4)")


    def test_autofill_of_add_form(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_the_manage_accounts_page()
        sel.click("css=tab_title")
        time.sleep(0.5)
        sel.type("css=#id_first_name", "Will Billerton")
        self.assertEqual(sel.get_value("css=#id_username"),"will")


    def test_disabling_of_add_button_until_the_form_is_valid(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_the_manage_accounts_page()
        sel.click("css=tab_title")
        time.sleep(0.5)
        assert sel.is_element_present("css=.create_account_btn.disabled")
        sel.click("css=.create_account_btn")
        sel.type("css=#id_first_name", "Joe Smith")
        assert sel.is_element_present("css=.create_account_btn.disabled")
        sel.click("css=.create_account_btn")
        sel.type("css=#id_username", "joe")
        assert sel.is_element_present("css=.create_account_btn.disabled")
        sel.click("css=.create_account_btn")
        sel.type("css=#id_password", "pass")
        assert sel.is_element_present("css=.create_account_btn.disabled")
        sel.click("css=.create_account_btn")
        sel.type("css=#id_email", "test@example.com")
        assert sel.is_element_present("css=.create_account_btn.disabled")
        sel.click("css=.create_account_btn")
        sel.click("css=#id_access_level_0")
        assert not sel.is_element_present("css=.create_account_btn.disabled")

        # try the reverse
        self.go_to_the_manage_accounts_page()
        sel.click("css=tab_title")
        time.sleep(0.5)
        assert sel.is_element_present("css=.create_account_btn.disabled")
        sel.click("css=.create_account_btn")
        sel.click("css=#id_access_level_2")
        assert sel.is_element_present("css=.create_account_btn.disabled")
        sel.click("css=.create_account_btn")
        sel.type("css=#id_email", "test@example.com")
        assert sel.is_element_present("css=.create_account_btn.disabled")
        sel.click("css=.create_account_btn")
        sel.type("css=#id_password", "pass")
        assert sel.is_element_present("css=.create_account_btn.disabled")
        sel.click("css=.create_account_btn")
        sel.type("css=#id_username", "joe")
        assert sel.is_element_present("css=.create_account_btn.disabled")
        sel.click("css=.create_account_btn")
        sel.type("css=#id_first_name", "Joe Smith")
        
        assert not sel.is_element_present("css=.create_account_btn.disabled")

    def test_that_staff_and_volunteers_can_not_see_the_account_link(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_the_login_page()
        self.log_in(username="staff", password="staff")
        assert not sel.is_element_present("css=.admin_btn")
        self.go_to_the_login_page()
        self.log_in(username="volunteer", password="volunteer")
        assert not sel.is_element_present("css=.admin_btn")
    
    def test_that_staff_and_volunteers_who_try_to_go_to_the_account_link_are_redirected_out(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_the_login_page()
        self.log_in(username="staff", password="staff")
        self.open(self.MANAGE_USERS_URL)
        sel.wait_for_page_to_load("30000")
        time.sleep(40)
        assert sel.is_element_present("css=salutation")

        self.go_to_the_login_page()
        self.log_in(username="volunteer", password="volunteer")
        self.open(self.MANAGE_USERS_URL)
        sel.wait_for_page_to_load("30000")
        assert sel.is_element_present("css=salutation")


    def test_that_editing_the_organization_name_works(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_the_account_page()
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.type("css=#id_name", "A new test name")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("A new test name")

    def test_that_editing_my_account_info_saves(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_my_account_page()
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.type("css=#id_first_name", "John Williams")
        sel.type("css=#id_email", "jwill@example.com")
        sel.type("css=#id_username", "jwill")
        sel.type("css=#id_nickname", "j-dog")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("John Williams")
        assert sel.is_text_present("jwill@example.com")
        assert sel.is_text_present("jwill")
        assert sel.is_text_present("j-dog")

    def test_that_changing_my_username_works_on_login(self):
        sel = self.selenium
        self.test_that_editing_my_account_info_saves()
        sel.click("css=.logout_btn")
        sel.wait_for_page_to_load("30000")
        sel.click("link=log back in")
        sel.wait_for_page_to_load("30000")
        self.log_in(username="jwill", password="admin")

    def test_that_changing_my_password_works_on_login(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_my_account_page()
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.click("css=.change_password_btn")
        time.sleep(0.25)
        sel.type("css=#id_new_password","test123")
        sel.click("css=#cancel_new_password_btn")
        sel.click("css=.change_password_btn")
        time.sleep(0.25)
        sel.type("css=#id_new_password","test123")
        sel.click("css=#save_new_password_btn")
        time.sleep(4)
        assert sel.is_text_present("New password saved.")
        sel.click("css=.logout_btn")
        sel.wait_for_page_to_load("30000")
        sel.click("link=log back in")
        sel.wait_for_page_to_load("30000")
        self.log_in(username="admin", password="test123")

    def test_staff_see_an_account_link(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_the_login_page()
        self.log_in(username="staff", password="staff")
        assert sel.is_element_present("css=.my_account_btn")
        assert not sel.is_element_present("css=.admin_btn")

    def test_volunteers_see_an_account_link(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_the_login_page()
        self.log_in(username="volunteer", password="volunteer")
        assert sel.is_element_present("css=.my_account_btn")
        assert not sel.is_element_present("css=.admin_btn")


    def admins_see_the_admin_link_and_not_an_account_link(self):
        sel = self.selenium
        self.setup_for_logged_in()
        assert not sel.is_element_present("css=.my_account_btn")
        assert sel.is_element_present("css=.admin_btn")

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
