import time 
from test_factory import Factory

from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase

class RulesTestAbstractions(object):

    pass


class TestAgainstNoData(QiConservativeSeleniumTestCase, RulesTestAbstractions):
    pass


class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions):
    # selenium_fixtures = ["200_test_people.json"]
    
    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
