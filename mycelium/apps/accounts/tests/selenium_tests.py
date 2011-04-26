# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from groups.tests.selenium_abstractions import GroupTestAbstractions
from django.conf import settings
from accounts.tests.selenium_abstractions import AccountTestAbstractions
    
class TestAgainstNoData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions, GroupTestAbstractions):
    # # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()
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
        self.go_to_the_login_page("test2")
        self.log_in(ua=ua)
        # sel.open("/people")

        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "joh smith 555")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")

        time.sleep(2)
        assert not sel.is_text_present("John Smith")


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

    def test_that_logging_in_takes_you_to_the_people_page(self):
        sel = self.selenium
        self.go_to_the_login_page()
        self.log_in()
        self.assert_login_succeeded()
        assert sel.is_element_present("link=New Person")

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
        time.sleep(2)

        sel.click("css=#submit_button")
        sel.wait_for_page_to_load("30000")
        assert not sel.is_element_present("css=#submit_button")
        self.go_to_the_login_page(site="tomsnonprofit")
        self.log_in(username="tom", password="Test123")


class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
