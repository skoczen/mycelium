# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_tests import PeopleTestAbstractions

class GroupTestAbstractions(object):

    def create_person_and_go_to_donor_tab(self):
        self.create_john_smith()
        self.switch_to_donor_tab()

class TestAgainstNoData(QiConservativeSeleniumTestCase, GroupTestAbstractions, PeopleTestAbstractions):

    def test_that_the_test_group_page_loads(self):
        sel = self.selenium
        sel.open("/people")
        sel.wait_for_page_to_load("30000")
        sel.click("link=New Group")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("All people who match")


class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, GroupTestAbstractions, PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    




