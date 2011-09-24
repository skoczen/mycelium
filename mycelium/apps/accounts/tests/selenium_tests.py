# encoding: utf-8
import unittest
import time
import datetime

from django.core.cache import cache
from django.core import mail
from django.core.urlresolvers import reverse
from johnny import cache as jcache
from django.test.client import Client
from django.template.defaultfilters import date
from django.conf import settings
from django.utils import simplejson
from functional_tests.selenium_test_case import DjangoFunctionalConservativeSeleniumTestCase
from zebra.signals import *

from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from organizations.tests.selenium_abstractions import OrganizationsTestAbstractions
from groups.tests.selenium_abstractions import GroupTestAbstractions
from dashboard.tests.selenium_abstractions import DashboardTestAbstractions
from accounts.models import Account
from accounts import *
from accounts.tests.selenium_abstractions import AccountTestAbstractions, _sitespaced_url
    
class TestAgainstLiterallyNoData(DjangoFunctionalConservativeSeleniumTestCase, PeopleTestAbstractions, OrganizationsTestAbstractions, AccountTestAbstractions, GroupTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.a1 = self.setup_for_logged_in_with_no_data()
        cache.clear()
        self.verificationErrors = []

    def test_setting_access_levels_for_a_user_stays(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.go_to_the_manage_accounts_page()

        # get my row
        for i in range(1,4):
            if sel.is_element_present("css=.user_row:nth(%s) .access_level label:nth(0) input:checked" % i):
                my_user = i
                break
        
        # make everyone else admins
        for i in range(1,4):
            if not i == my_user:
                assert not sel.is_element_present("css=.user_row:nth(%s) .access_level label:nth(0) input:checked" % (i,))
                sel.click("css=.user_row:nth(%s) .access_level input:nth(0)" % (i,))

        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(1,4):
            if not i == my_user:
                assert sel.is_element_present("css=.user_row:nth(%s) .access_level label:nth(0) input:checked" % (i,))

        # make everyone else staff
        for i in range(1,4):
            if not i == my_user:
                assert not sel.is_element_present("css=.user_row:nth(%s) .access_level label:nth(1) input:checked" % (i,))
                sel.click("css=.user_row:nth(%s) .access_level input:nth(1)" % (i,))

        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(1,4):
            if not i == my_user:
                assert sel.is_element_present("css=.user_row:nth(%s) .access_level label:nth(1) input:checked" % (i,))

        # make everyone else a volunteer
        for i in range(1,4):
            if not i == my_user:
                assert not sel.is_element_present("css=.user_row:nth(%s) .access_level label:nth(2) input:checked" % (i,))
                sel.click("css=.user_row:nth(%s) .access_level input:nth(2)" % (i,))

        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        for i in range(1,4):
            if not i == my_user:
                assert sel.is_element_present("css=.user_row:nth(%s) .access_level label:nth(2) input:checked" % (i,))



class TestAgainstNoData(DjangoFunctionalConservativeSeleniumTestCase, PeopleTestAbstractions, OrganizationsTestAbstractions, AccountTestAbstractions, GroupTestAbstractions):
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
        cache.clear()
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
        time.sleep(10)
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
        
        for i in range(1,4):
            if "Joe Smith" == sel.get_text("css=.user_row:nth(%s) .full_name" % i):
                john_smith_row = i
                break

        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.user_row:nth(%s) .reset_password_btn" % john_smith_row )
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to reset the password for Joe Smith?\n\nClick OK to reset their password.\nClick Cancel to leave it unchanged.\n")
        sel.click("css=.user_row:nth(%s) .reset_password_btn" % john_smith_row )
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
        for i in range(1,4):
            if sel.is_element_present("css=.user_row:nth(%s) .access_level label:nth(0) input:checked" % i):
                my_user = i
                break
        
        sel.click("css=.user_row:nth(%s) .delete_user_btn" % my_user)
        sel.get_confirmation()
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Welcome to GoodCloud")
        

    def test_deleting_a_user(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.create_a_new_user_via_manage_accounts()
        assert sel.is_element_present("css=.user_row:nth(4)")
        
        for i in range(1,4):
            if "Joe Smith" == sel.get_text("css=.user_row:nth(%s) .full_name" % i):
                john_smith_row = i
                break

        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.user_row:nth(%s) .delete_user_btn" % (john_smith_row,))
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to delete the account for Joe Smith?\n\nThis is permanent, but will not affect any data besides their account.\n\nClick OK to delete the account.\nClick Cancel to leave it alone.\n")
        sel.click("css=.user_row:nth(%s) .delete_user_btn" % (john_smith_row,))
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


    def test_admins_see_the_admin_link_and_not_an_account_link(self):
        sel = self.selenium
        self.get_logged_in()
        assert sel.is_element_present("css=.admin_btn")


    @unittest.skip("This fails because it doesn't 'somehow' resubmit. Problem with the test, not the functionality.  TODO? ")
    def test_that_somehow_resubmitting_an_existing_account_subdomain_redirects_to_their_login_page(self):
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
        self.test_that_the_account_signup_page_loads()
        sel.type("css=#id_name","My Test Organization")
        sel.type("css=#id_subdomain","test2")
        sel.focus("css=#id_subdomain")

        sel.type("css=#id_first_name","Joe Tester")
        sel.type("css=#id_email", "joe@example.com")
        sel.type("css=#id_username", "joe")
        sel.type("css=#id_password", "password")
        sel.click("css=#id_agreed_to_terms")
        sel.click("css=#submit_button")

        # sel.wait_for_page_to_load("30000")

        # self.go_to_the_login_page(site="test2")
        self.log_in(username="joe", password="password")



class TestSubscriptionsAgainstNoData(DjangoFunctionalConservativeSeleniumTestCase, DashboardTestAbstractions):
    # selenium_fixtures = []
    # # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()
        self.account = self.a1
        cache.clear()
        self.verificationErrors = []


    def test_that_new_signups_see_their_status_as_free_trial(self):
        sel = self.selenium
        self.get_logged_in()
        self.go_to_the_account_page()
        assert sel.is_text_present("Status: Free Trial")
    
    def test_that_new_signups_see_the_correct_signup_date(self):
        sel = self.selenium
        self.get_logged_in()
        self.go_to_the_account_page()
        assert sel.is_text_present("Signup Date: %s" % (date(datetime.date.today()),) )

    
    def test_that_the_free_trial_date_is_adjusted_after_finishing_all_dashboard_tasks(self):
        sel = self.selenium
        self.get_logged_in()
        self.go_to_the_account_page()
        print "Free Trial until %s" % (date(datetime.date.today()+datetime.timedelta(days=30)),)
        assert sel.is_text_present("Free Trial until %s" % (date(datetime.date.today()+datetime.timedelta(days=30)),) )

        self.create_another_account()
        self.import_contacts()
        self.add_volunteer_shift()
        self.add_donation()
        self.create_tag_and_tag_a_board_member()
        self.create_a_spreadsheet()
        self.get_to_the_dashboard()

        self.go_to_the_account_page()
        assert sel.is_text_present("Free Trial until %s" % (date(datetime.date.today()+datetime.timedelta(days=44)),) )
        self.assertEqual(datetime.date.fromtimestamp(self.account.stripe_subscription.trial_end), datetime.date.today() + datetime.timedelta(days=44))


    def test_that_new_signups_can_sign_up_for_an_account(self):
        sel = self.selenium
        self.get_logged_in()
        self.go_to_the_account_page()
        self.enter_billing_info_signup()

        assert sel.is_text_present("Status: Free Trial")
        assert sel.is_text_present("XXXX-XXXX-XXXX-%s" % (Factory.test_cc_number(True)[-4:]))
        assert sel.is_text_present("Signup Date: %s" % (date(datetime.date.today()),) )
        assert sel.is_element_present("link=Update Billing Information")


    def test_that_after_signup_users_can_change_their_billing_info(self):
        # And see it updated.
        sel = self.selenium
        self.get_logged_in()
        self.go_to_the_account_page()

        self.enter_billing_info_signup()
        assert sel.is_text_present("XXXX-XXXX-XXXX-%s" % (Factory.test_cc_number(True)[-4:]))
        
        self.enter_billing_info_signup(cc_number="4222222222222")
        assert not sel.is_text_present("XXXX-XXXX-XXXX-%s" % (Factory.test_cc_number(True)[-4:]))
        assert sel.is_text_present("XXXX-XXXX-XXXX-2222")

    @unittest.skip("This passes by hand, but appears to have some selenium / js conflicts for FF.")
    def test_that_users_cannot_enter_invalid_cc_info(self):
        sel = self.selenium
        self.get_logged_in()
        self.go_to_the_account_page()

        assert not sel.is_text_present("Your card number is incorrect.")
        self.enter_billing_info_signup(valid_cc=False)
        time.sleep(60)
        assert sel.is_text_present("Your card number is incorrect.")

    @unittest.skip("TODO: When stripe properly supports test data, wire this up with it.")
    def test_that_after_the_free_trial_ends_a_non_cc_user_moves_to_billing_problem(self):
        sel = self.selenium
        self.get_logged_in()
        self.go_to_the_account_page()
        assert sel.is_text_present("Status: Free Trial")

        c = self.account.stripe_customer
        c.update_subscription(plan=MONTHLY_PLAN_NAME, trial_end=datetime.datetime.now()+datetime.timedelta(seconds=4))
        self.go_to_the_account_page()

        assert not sel.is_text_present("Status: Free Trial")


    def test_expired_accounts_display_an_expired_bar(self):
        sel = self.selenium
        a = self.a1
        a.signup_date = datetime.datetime.now() - datetime.timedelta(days=35)
        a.status = STATUS_ACTIVE_BILLING_ISSUE
        a.save()
        self.get_logged_in()
        
        # assert sel.is_element_present(".expired_bar")
        assert sel.is_element_present("css=#expired_side_bar")


    
    def test_expired_accounts_display_a_human_explanation_on_the_billing_page(self):
        sel = self.selenium
        self.test_expired_accounts_display_an_expired_bar()
        self.go_to_the_account_page()
        assert sel.is_text_present("problem processing your billing method")
    

    def test_deactivated_accounts_display_a_human_explanation_on_the_billing_page(self):
        sel = self.selenium
        a = self.a1
        a.status = STATUS_DEACTIVATED
        a.save()
        
        self.get_logged_in()

        self.go_to_the_account_page()
        assert sel.is_element_present("css=#expired_side_bar")
        assert sel.is_text_present("Your account has been deactivated")

    def test_that_after_a_successful_charge_accounts_are_moved_to_active(self):
        # And see it updated.
        sel = self.selenium
        self.get_logged_in()
        self.go_to_the_account_page()
        assert sel.is_text_present("Status: Free Trial")
        self.enter_billing_info_signup()
        c = self.a1.stripe_customer
        c.update_subscription(plan=MONTHLY_PLAN_NAME, trial_end=datetime.datetime.now()+datetime.timedelta(seconds=4))
        time.sleep(60)
        self.a1.update_account_status()
        cache.clear()
        self.go_to_the_account_page()

        assert not sel.is_text_present("Status: Free Trial")
        assert sel.is_text_present("Status: Active")



    def test_users_can_completely_delete_their_account(self):
        sel = self.selenium
        a_pk = self.a1.pk
        
        self.get_logged_in()
        self.go_to_the_account_page()
        self.assertEqual(Account.objects.filter(pk=a_pk).count(),1)
        
        sel.click("css=.account_delete_btn")
        sel.wait_for_page_to_load("30000")
        sel.click("css=.do_account_delete_btn")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("We're sad to see you go, but we understand.")

       
        self.go_to_the_login_page("test")
        assert not sel.is_text_present ("Log In")

        # self.assertEqual(Account.objects.filter(pk=a_pk).count(),0)


    def test_that_clicking_get_me_outta_here_does_that(self):
        sel = self.selenium
        self.get_logged_in()
        self.go_to_the_account_page()
        sel.click("css=.account_delete_btn")
        sel.wait_for_page_to_load("30000")
        sel.click("css=.outta_here")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("My Account")



class TestAgainstGeneratedData(DjangoFunctionalConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
    
