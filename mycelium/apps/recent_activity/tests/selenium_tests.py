# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time 
from test_factory import Factory

from people.tests.selenium_tests import PeopleTestAbstractions

class RecentActivityTestAbstractions(object):

    def create_person_and_go_to_recent_activity_tab(self):
        sel = self.selenium
        self.create_john_smith()
        sel.click("css=.detail_tab[href=#recent_activity]")
        time.sleep(1)

class TestAgainstNoData(QiConservativeSeleniumTestCase, RecentActivityTestAbstractions, PeopleTestAbstractions):



    def test_recent_activity_tab_is_a_stub(self):
        sel = self.selenium
        self.create_person_and_go_to_recent_activity_tab()
        assert sel.is_text_present("Recent Activity's not done quite yet, but it's coming!")

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, RecentActivityTestAbstractions, PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    

