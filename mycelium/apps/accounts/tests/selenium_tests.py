# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_tests import PeopleTestAbstractions

class AccountTestAbstractions(object):
    def create_demo_site_and_log_in(self):
        from django.conf import settings
        Factory.create_demo_site("test",quick=True)
        sel = self.selenium
        sel.open("http://test.localhost:%s" % settings.LIVE_SERVER_PORT)
        sel.wait_for_page_to_load("30000")
        sel.type("css=input[name=username]","admin")
        sel.type("css=input[name=password]","admin")
        sel.click("css=.login_btn")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Powered by")

class TestAgainstNoData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.verificationErrors = []


    def test_that_logging_in_works(self):
        sel = self.selenium
        self.create_demo_site_and_log_in()
        assert sel.is_text_present("Powered by")

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        
        self.verificationErrors = []
    
