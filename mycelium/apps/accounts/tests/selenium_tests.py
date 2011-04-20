# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions

class AccountTestAbstractions(object):
    def create_demo_site(self, name="test"):
        return Factory.create_demo_site(name,quick=True)

    def go_to_the_login_page(self, site="test"):
        from django.conf import settings
        sel = self.selenium
        sel.open("http://%s.localhost:%s" % (site,settings.LIVE_SERVER_PORT))
        sel.wait_for_page_to_load("30000")

    def log_in(self, ua=None):
        if not ua:
            username = "admin"
        else:
            username = ua.denamespaced_username
        sel = self.selenium
        sel.type("css=input[name=username]",username)
        sel.type("css=input[name=password]",username)
        sel.click("css=.login_btn")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Powered by")
    
    def assert_login_failed(self):
        sel = self.selenium
        assert sel.is_text_present("Your username and password didn't match")

    def assert_login_succeeded(self):
        sel = self.selenium
        assert sel.is_text_present("Powered by")

    def open(self, url, site="test"):
        from django.conf import settings
        sel = self.selenium
        sel.open("http://%s.localhost:%s%s" % (site,settings.LIVE_SERVER_PORT,url))
        sel.wait_for_page_to_load("30000")

    
class TestAgainstNoData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.create_demo_site()
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
        self.log_in(ua=ua)
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
        self.open("/people", site="test2")
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
    
    def test_that_searching_across_accounts_limits_results(self):
        pass



    def test_fixed_switching_accounts_on_search_shows_the_wrong_orgs_results_until_thread_change(self):
        """Yep, this happens - make demo and demo1, view demo, then type demo1 in the address bar and load - 
            voila - demo's results :(
            Classmethod caching?

            # SESSION_SAVE_EVERY_REQUEST = True helps but doesn't fix.

            Not true anymore.  There was just a simple bug in the middleware that just gave the wrong account.
        """ 
        assert False == True


    def test_that_requesting_an_invalid_person_404s(self):
        assert True == "Written"
    
    def test_that_requesting_an_invalid_organization_404s(self):
        assert True == "Written"

    def test_that_requesting_an_invalid_group_404s(self):
        assert True == "Written"

    

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        
        self.verificationErrors = []
    
