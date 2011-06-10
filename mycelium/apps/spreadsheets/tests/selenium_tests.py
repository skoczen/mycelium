from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from spreadsheets.tests.selenium_abstractions import SpreadsheetTestAbstractions
import time

class TestSelenium(QiConservativeSeleniumTestCase, SpreadsheetTestAbstractions, AccountTestAbstractions):
    selenium_fixtures = []

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
    
    def test_spreadsheet_search_loads(self):
        self.get_to_spreadsheets_page()
        self.assert_on_spreadsheet_search_page()

    def test_clicking_the_new_spreadsheet_button_takes_you_to_a_new_spreadsheet(self):
        sel = self.selenium
        self.get_to_spreadsheets_page()
        sel.click("link=New Spreadsheet")
        sel.wait_for_page_to_load("30000")
        self.assert_on_edit_spreadsheet_page()


    def test_creating_a_new_spreadsheet_saves(self):
        sel = self.selenium
        self.test_clicking_the_new_spreadsheet_button_takes_you_to_a_new_spreadsheet()
        sel.type("css=#id_name", "My test spreadsheet")
        time.sleep(6)
        sel.refresh()
        assert sel.is_text_present("My test spreadsheet")
        sel.click("link=Back to Spreadsheets")
        sel.wait_for_page_to_load("30000")
        self.assert_on_spreadsheet_search_page()
        assert sel.is_text_present("My test spreadsheet")
        
    
    def test_changing_the_name_group_and_type_of_a_spreadsheet_works(self):
        sel = self.selenium
        self.test_creating_a_new_spreadsheet_saves()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.type("css=#id_name", "Actually, I decided on a new name.")
        sel.select("css=#id_group", "Board of Directors")
        sel.select("css=#id_spreadsheet_template", "Mailing List")
        sel.click("css=label[for=id_default_filetype_1]")
        sel.click("css=.save_and_status_btn")
        time.sleep(2)
        sel.refresh()
        assert sel.is_text_present("Actually, I decided on a new name.")
        assert sel.is_text_present("Board of Directors")
        assert sel.is_text_present("Mailing List.")

    def test_that_all_and_only_all_of_the_groups_are_listed(self):
        pass
    
    def test_that_searching_for_a_spreasheet_works(self):
        pass
    
    def test_that_deleting_a_spreadsheet_works(self):
        pass