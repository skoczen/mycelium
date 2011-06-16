# encoding: utf-8
import time
from test_factory import Factory


class SpreadsheetTestAbstractions(object):
    def get_to_spreadsheets_page(self):
        sel = self.selenium
        self.open("/people/search")
        sel.click("link=Spreadsheets")
        sel.wait_for_page_to_load("30000")

    def assert_on_edit_spreadsheet_page(self):
        sel = self.selenium
        assert sel.is_text_present("Download Spreadsheet")

    def assert_on_spreadsheet_search_page(self):
        sel = self.selenium
        assert sel.is_element_present("css=#id_search_query")
        assert sel.is_element_present("link=New Spreadsheet")
    

    def start_a_new_spreadsheet(self):
        sel = self.selenium
        self.get_to_spreadsheets_page()
        sel.click("link=New Spreadsheet")
        sel.wait_for_page_to_load("30000")
        self.assert_on_edit_spreadsheet_page()

    
    def create_a_spreadsheet(self, name="My test spreadsheet"):
        sel = self.selenium
        self.start_a_new_spreadsheet()
        sel.type("css=#id_name", name)
        time.sleep(6)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present(name)
        sel.click("css=.back_to_search_btn")
        sel.wait_for_page_to_load("30000")
        self.assert_on_spreadsheet_search_page()
        assert sel.is_text_present(name)
        sel.click("link=%s" % name)
        sel.wait_for_page_to_load("30000")
