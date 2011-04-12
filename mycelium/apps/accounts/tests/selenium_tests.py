# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_tests import PeopleTestAbstractions

class AccountTestAbstractions(object):
    pass

class TestAgainstNoData(QiConservativeSeleniumTestCase, PeopleTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.verificationErrors = []

    # def test_that_the_new_group_page_loads(self):
    #     sel = self.selenium
    #     self.create_new_group()
    #     assert sel.is_text_present("the following rules")

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions):
    selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.people = [Factory.volunteer_history() for i in range(1,Factory.rand_int(30,100))]
        self.verificationErrors = []
    
