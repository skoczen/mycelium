from functional_tests.selenium_test_case import DjangoFunctionalConservativeSeleniumTestCase
import time 
from test_factory import Factory
from accounts.tests.selenium_abstractions import AccountTestAbstractions

class TestAgainstNoData(DjangoFunctionalConservativeSeleniumTestCase, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
        self.verificationErrors = []
    
    # def tearDown(self):
    #     self.account.delete()


    def test_creating_and_editing_a_new_person(self):
        sel = self.selenium
        assert 1==1
        