from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
from accounts.tests.selenium_abstractions import AccountTestAbstractions

class ReportsTests(QiConservativeSeleniumTestCase):
    def get_to_reports_page(self):
        sel = self.selenium
        self.open("/people/search")
        sel.click("link=More")
        sel.wait_for_page_to_load("30000")
        sel.click("css=.reports_btn")
        sel.wait_for_page_to_load("30000")


class TestSelenium(ReportsTests, AccountTestAbstractions):
    selenium_fixtures = []

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
    
    # def tearDown(self):
    #     self.account.delete()


    
    def test_all_pages_load(self):
        sel = self.selenium
        self.get_to_reports_page()
        sel.wait_for_page_to_load("30000")
        sel.click("link=Thursday Volunteer List")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Thursday Volunteer List")
        self.assertEqual("Add new criteria", sel.get_text("link=Add new criteria"))
        sel.click("link=Back to All Spreadsheets")
        sel.wait_for_page_to_load("30000")
        sel.click("link=New Spreadsheet")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Save Spreadsheet", sel.get_text("link=Save Spreadsheet"))
