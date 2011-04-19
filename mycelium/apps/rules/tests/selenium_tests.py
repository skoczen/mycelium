import time 
from test_factory import Factory

from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase

class RulesTestAbstractions(object):

    pass


class TestAgainstNoData(QiConservativeSeleniumTestCase, RulesTestAbstractions):
    pass


class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, RulesTestAbstractions):
    # selenium_fixtures = ["200_test_people.json"]
    
    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()
        self.verificationErrors = []
