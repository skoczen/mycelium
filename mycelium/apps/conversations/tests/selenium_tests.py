from djangosanetesting.cases import SeleniumTestCase
import time 
from test_factory import Factory
from django.core.management import call_command

class TestAgainstNoData(SeleniumTestCase):
    def setUp(self):
        self.verificationErrors = []
    
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)
        call_command('flush', interactive=False)




class TestAgainstGeneratedData(SeleniumTestCase):

    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    
    def tearDown(self,*args, **kwargs):
        call_command('flush', interactive=False)
        self.assertEqual([], self.verificationErrors)
