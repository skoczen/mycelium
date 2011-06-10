from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from spreadsheets.tests.selenium_abstractions import SpreadsheetTestAbstractions

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
