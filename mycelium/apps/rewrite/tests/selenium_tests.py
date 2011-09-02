# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
import datetime
from test_factory import Factory
from rewrite.tests.selenium_abstractions import RewriteTestAbstractions
from accounts.models import Account
from django.conf import settings
from django.core.cache import cache
from django.template.defaultfilters import date
    
class TestRewriteManagement(QiConservativeSeleniumTestCase, RewriteTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.verificationErrors = []

    def test_creating_a_page(self):
        self.get_to_management_console()
        self.log_in(username="admin")   



class TestRewriteBlog(QiConservativeSeleniumTestCase, RewriteTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
    
class TestRewritePage(QiConservativeSeleniumTestCase, RewriteTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
    
        