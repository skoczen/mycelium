from djangosanetesting.cases import SeleniumTestCase
import time 
from test_factory import Factory

class TestAgainstNoData(SeleniumTestCase):
    selenium_fixtures = []
    
    def setUp(self):
        self.verificationErrors = []
    
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    def test_creating_and_editing_a_new_person(self):
        sel = self.selenium
        assert 1==1
        