# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_tests import PeopleTestAbstractions

class TagTestAbstractions(object):
    def switch_to_tag_tab():
        sel = self.selenium
        sel.click("css=.detail_tab[href=#tags]")
        time.sleep(3)

    def create_person_and_go_to_tag_tab(self):
        self.create_john_smith()
        self.switch_to_tag_tab()

class TestAgainstNoData(QiConservativeSeleniumTestCase, TagTestAbstractions, PeopleTestAbstractions):
    pass

    def test_that_tags_tab_displays(self):
        self.create_person_and_go_to_tag_tab()
        assert sel.is_text_present("General")

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, TagTestAbstractions, PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    

