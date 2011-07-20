# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
import datetime
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from organizations.tests.selenium_abstractions import OrganizationsTestAbstractions
from groups.tests.selenium_abstractions import GroupTestAbstractions
from flight_control.tests.selenium_abstractions import FlightControlTestAbstractions
from django.conf import settings
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from django.core.cache import cache
from django.template.defaultfilters import date
    
class TestAgainstNoData(QiConservativeSeleniumTestCase, FlightControlTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()
        cache.clear()
        self.create_fake_account_for_flight_control()
        self.verificationErrors = []

    def test_that_flight_control_loads(self):
        self.get_to_flight_control()

    def test_that_flight_control_doesnt_load_for_another_user(self):
        sel = self.selenium
        sel.open("http://dashboard.localhost:%s" % settings.LIVE_SERVER_PORT)
        sel.wait_for_page_to_load("30000")
        sel.type("css=#id_username", "test")
        sel.type("css=#id_password", "test")
        sel.click("css=input[type=submit]")
        sel.wait_for_page_to_load("30000")
        assert not sel.is_text_present("GoodCloud Flight Control")

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, FlightControlTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
