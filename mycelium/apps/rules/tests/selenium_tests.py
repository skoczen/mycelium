import time 
from test_factory import Factory

from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase

class RulesTestAbstractions(object):

    pass


class TestAgainstNoData(QiConservativeSeleniumTestCase, RulesTestAbstractions):
    
    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_tests_with_no_data()


class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, RulesTestAbstractions):
    # selenium_fixtures = ["200_test_people.json"]
    
    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_tests()
        self.verificationErrors = []
