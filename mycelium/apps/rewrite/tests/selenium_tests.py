# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from rewrite.tests.selenium_abstractions import RewriteTestAbstractions
    
class TestRewriteManagement(QiConservativeSeleniumTestCase, RewriteTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.verificationErrors = []

    def test_management_console_loads(self):
        self.get_to_management_console()
        self.assert_in_the_management_console()

    def test_creating_a_section(self):
        self.create_a_section(name="My Test Section")

    def test_creating_a_page(self):
        self.create_a_section()
        self.create_a_page(name="My Test Page")
        
    def test_that_a_created_page_is_viewable_to_an_editor(self):
        self.create_a_section(name="Section To Test")
        self.create_a_page(name="My Test Page")
        self.open_page_publicly(name="My Test Page", section="Section To Test")
        time.sleep(50)



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
    
    
        