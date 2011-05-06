from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time 
from test_factory import Factory
from accounts.tests.selenium_abstractions import AccountTestAbstractions

class TestMockupPages(QiConservativeSeleniumTestCase, AccountTestAbstractions):
    selenium_fixtures = []

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()

    # def tearDown(self):
    #     self.account.delete()

    def test_mockup_pages_load_and_links_work(self):
        sel = self.selenium        
        self.open("/reports/report/new")
        sel.click("link=Admin")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Data Import", sel.get_text("css=.data_import_btn .button_title"))
        
        sel.click("css=.data_import_btn")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Data Import History", sel.get_text("//div[@id='page']/page_title"))
        self.assertEqual("Start New Import", sel.get_text("link=Start New Import"))
  
        self.assertEqual("View Results", sel.get_text("link=View Results"))
        
        self.assertEqual("Right now", sel.get_text("css=.in_progress .right_now"))
        
        sel.click("link=View Results")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Data Import #5 on Dec 29, 2010 at 3:55pm", sel.get_text("//div[@id='page']/page_title"))
        
        self.assertEqual("We found 2,937 people.", sel.get_text("css=.report_summary .total"))
        
        self.assertEqual("Back to All Data Imports", sel.get_text("link=Back to All Data Imports"))
        
        sel.click("link=Back to All Data Imports")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Start New Import", sel.get_text("link=Start New Import"))
        
        sel.click("link=Start New Import")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Back to All Data Imports", sel.get_text("link=Back to All Data Imports"))
        
        self.assertEqual("Start Data Import", sel.get_text("//div[@id='page']/page_title"))
        
        self.assertEqual("Choose a CSV Spreadsheet.", sel.get_text("css=step[number=1] instruction"))
        
        self.assertEqual("Start Import", sel.get_text("link=Start Import"))
        
        sel.click("link=Back to All Data Imports")
        sel.wait_for_page_to_load("30000")