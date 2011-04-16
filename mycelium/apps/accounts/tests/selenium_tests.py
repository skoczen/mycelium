# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_tests import PeopleTestAbstractions

class AccountTestAbstractions(object):
    def create_demo_site(self, name="test"):
        return Factory.create_demo_site(name,quick=True)

    def go_to_the_login_page(self, site="test"):
        from django.conf import settings
        sel = self.selenium
        sel.open("http://%s.localhost:%s" % (site,settings.LIVE_SERVER_PORT))
        sel.wait_for_page_to_load("30000")

    def log_in(self):
        sel = self.selenium
        self.go_to_the_login_page()
        sel.type("css=input[name=username]","admin")
        sel.type("css=input[name=password]","admin")
        sel.click("css=.login_btn")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Powered by")
    
    def assert_login_failed(self):
        sel = self.selenium
        assert sel.is_text_present("Your username and password didn't match")

    def assert_login_succeeded(self):
        sel = self.selenium
        assert sel.is_text_present("Powered by")

class TestAgainstNoData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.create_demo_site()
        self.verificationErrors = []


    def test_that_logging_in_works(self):
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
        sel.open("/people")
        assert sel.is_element_present("css=.login_btn")

    def test_that_site2s_user_cannot_log_into_site_one(self):
        a2 = self.create_demo_site("test2")
        sel = self.selenium
        self.go_to_the_login_page()
        ua = Factory.useraccount(account=a2)
        sel.type("css=input[name=username]",ua.denamespaced_username)
        sel.type("css=input[name=password]",ua.denamespaced_username)
        sel.click("css=.login_btn")
        sel.wait_for_page_to_load("30000")
        self.assert_login_failed()

        self.go_to_the_login_page("test2")
        sel.type("css=input[name=username]",ua.denamespaced_username)
        sel.type("css=input[name=password]",ua.denamespaced_username)
        sel.click("css=.login_btn")
        sel.wait_for_page_to_load("30000")
        self.assert_login_succeeded()

    def test_that_site2s_user_cannot_manually_browse_to_site_ones_page(self):
        pass

    def test_that_a_new_person_in_account_1_does_not_show_in_account_2(self):
        pass
    
    def test_that_searching_across_accounts_limits_results(self):
        pass

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        
        self.verificationErrors = []
    
