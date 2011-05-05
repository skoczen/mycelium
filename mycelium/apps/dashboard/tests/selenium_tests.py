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

    def test_that_saying_yes_to_a_nickname_works(self):
        assert True == "Test written"
 
    def test_that_saying_no_and_providing_a_new_nickname_works(self):
        assert True == "Test written"

    def test_that_the_dashboard_checks_off_appropriately(self):
        assert True == "Test written"

    def test_that_the_by_the_numbers_numbers_are_accurate(self):
        # compare shown numbers vs hand-cound.
        assert True == "Test written"

    def test_the_nothing_done_on_the_checklist_welcome_text(self):
        assert True == "Test written"

    def test_the_something_done_on_the_checklist_welcome_text(self):
        assert True == "Test written"



class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
