# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time 
from test_factory import Factory

from people.tests.selenium_tests import PeopleTestAbstractions


class TestAgainstNoData(QiConservativeSeleniumTestCase):
    pass


    # def test_404(self):
    #     sel = self.selenium        
    #     sel.open("/dfiua09zjvbnoizllkq3")
    #     sel.wait_for_page_to_load("30000")
    #     assert sel.is_text_present("we don't have that page")

    # def test_500(self):
    #     sel = self.selenium
    #     sel.open("always_500")
    #     sel.wait_for_page_to_load("30000")
    #     assert sel.is_text_present("problems loading that page")
