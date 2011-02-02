from djangosanetesting.cases import SeleniumTestCase
import time 
from test_factory import Factory

class TestMockupPages(SeleniumTestCase):
    selenium_fixtures = []
    
    def setUp(self):
        self.verificationErrors = []
    
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)


    def test_mockup_pages_load_and_links_work(self):
        sel = self.selenium        
        sel.open("/reports/report/new")
        sel.click("link=More")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Data Import", sel.get_text("css=.data_import_btn .button_title"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=.data_import_btn")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Data Import History", sel.get_text("//div[@id='page']/page_title"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Start New Import", sel.get_text("link=Start New Import"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("", sel.get_text("//div[@id='page']/record_list/table/tbody/tr[1]/td[1]/img"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("View Results", sel.get_text("link=View Results"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Right now", sel.get_text("//div[@id='page']/record_list/table/tbody/tr[1]/td[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=View Results")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Data Import #5 on Dec 29, 2010 at 3:55pm", sel.get_text("//div[@id='page']/page_title"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("We found 2,937 people.", sel.get_text("//div[@id='page']/div/div[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Back to All Data Imports", sel.get_text("link=Back to All Data Imports"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Back to All Data Imports")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Start New Import", sel.get_text("link=Start New Import"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Start New Import")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Back to All Data Imports", sel.get_text("link=Back to All Data Imports"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Start Data Import", sel.get_text("//div[@id='page']/page_title"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Choose a CSV Spreadsheet", sel.get_text("//div[@id='page']/div[2]/step[1]/instruction"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Start Import", sel.get_text("link=Start Import"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Back to All Data Imports")
        sel.wait_for_page_to_load("30000")