# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
import datetime
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from organizations.tests.selenium_abstractions import OrganizationsTestAbstractions
from rewrite.tests.selenium_abstractions import RewriteTestAbstractions
from accounts.models import Account
from django.conf import settings
from accounts.tests.selenium_abstractions import AccountTestAbstractions

from django.core.cache import cache
from django.template.defaultfilters import date
    
class TestAgainstNoData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, OrganizationsTestAbstractions, AccountTestAbstractions, RewriteTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.a1 = self.setup_for_logged_in_with_no_data()
        cache.clear()
        self.verificationErrors = []

    # def test_setting_access_levels_for_a_user_stays(self):
    #     sel = self.selenium
    #     self.setup_for_logged_in()
    #     self.go_to_the_manage_accounts_page()





class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
    
        