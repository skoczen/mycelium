
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
        assert sel.is_element_present("css=.title")
        assert sel.is_element_present("link=New Spreadsheet")