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

    

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
