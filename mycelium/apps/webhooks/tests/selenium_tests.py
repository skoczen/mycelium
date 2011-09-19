# encoding: utf-8
from functional_tests.selenium_test_case import DjangoFunctionalConservativeSeleniumTestCase
import time
from test_factory import Factory
from webhooks.tests.selenium_abstractions import WebhookTestAbstractions
from django.core.cache import cache
    
class TestAgainstLiterallyNoData(DjangoFunctionalConservativeSeleniumTestCase, WebhookTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.a1 = self.setup_for_logged_in_with_no_data()
        cache.clear()
        self.verificationErrors = []
    
    

class TestAgainstNoData(DjangoFunctionalConservativeSeleniumTestCase, WebhookTestAbstractions):
    # # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.setup_for_logged_in_with_no_data()
        
        self.verificationErrors = []

    

class TestAgainstGeneratedData(DjangoFunctionalConservativeSeleniumTestCase, WebhookTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
