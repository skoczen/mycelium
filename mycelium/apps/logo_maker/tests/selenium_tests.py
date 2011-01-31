from djangosanetesting.cases import SeleniumTestCase
import time 
from test_factory import Factory

class TestAgainstNoData(SeleniumTestCase):
    fixtures = []
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_creating_and_editing_a_new_person(self):
        sel = self.selenium
        