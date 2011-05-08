# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from groups.tests.selenium_abstractions import GroupTestAbstractions
from django.conf import settings
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from dashboard.tests.selenium_abstractions import DashboardTestAbstractions
    
class TestAgainstNoData(QiConservativeSeleniumTestCase, AccountTestAbstractions, DashboardTestAbstractions):
    # # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()
        self.verificationErrors = []

    def test_that_logging_in_goes_to_the_dashboard(self):
        sel = self.selenium
        self.setup_for_logged_in()
        assert sel.is_text_present("Hello") or sel.is_text_present("Hi")

    def test_that_saying_yes_to_a_nickname_works(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.get_to_the_dashboard()
        full_name = sel.get_text("css=.full_name")
        first_name = full_name[:full_name.find(" ")]
        sel.click("css=.yes_to_nickname")
        time.sleep(2)
        assert sel.is_text_present("Thanks, %s" % (first_name,) )
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Hi %s" % (first_name,) )
        assert not sel.is_element_present("css=.yes_to_nickname")

 
    def test_that_saying_no_and_providing_a_new_nickname_works(self):
        sel = self.selenium
        self.setup_for_logged_in()
        self.get_to_the_dashboard()
        sel.click("css=.no_to_nickname")
        time.sleep(0.25)
        sel.type("css=#id_new_nickname", "Jessy")
        sel.click("css=.save_new_nickname")
        time.sleep(2)
        assert sel.is_text_present("Thanks, Jessy")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Hi Jessy,")

    def test_that_the_dashboard_checks_off_appropriately(self):
        assert True == "Test written"

    def test_that_hiding_challenges_complete_hides_them(self):
        assert True == "Test written"        

    def test_the_nothing_done_on_the_checklist_welcome_text(self):
        assert True == "Test written"

    def test_the_something_done_on_the_checklist_welcome_text(self):
        assert True == "Test written"



class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, AccountTestAbstractions, DashboardTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
