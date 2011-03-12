# encoding: utf-8
from djangosanetesting.cases import SeleniumTestCase
import time 
from test_factory import Factory
from django.core.management import call_command
from people.tests.selenium_tests import PeopleTestAbstractions


class TestAgainstNoData(SeleniumTestCase):
    def setUp(self):
        self.verificationErrors = []
    
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)
        call_command('flush', interactive=False)


    def test_404(self):
        sel = self.selenium        
        sel.open("/dfiua09zjvbnoizllkq3")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("we don't have that page")

    def test_500(self):
        sel = self.selenium
        sel.open("always_500")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("problems loading that page")
