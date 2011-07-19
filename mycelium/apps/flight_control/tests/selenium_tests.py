# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
import datetime
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from organizations.tests.selenium_abstractions import OrganizationsTestAbstractions
from groups.tests.selenium_abstractions import GroupTestAbstractions
from django.conf import settings
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from django.core.cache import cache
from django.template.defaultfilters import date
    
class TestAgainstNoData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, OrganizationsTestAbstractions, AccountTestAbstractions, GroupTestAbstractions):
    # selenium_fixtures = []
    # # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()
        cache.clear()
        self.verificationErrors = []

    # def test_that_logging_in_works(self):
    #     self.go_to_the_login_page()
    #     self.log_in()
    #     self.assert_login_succeeded()


class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
