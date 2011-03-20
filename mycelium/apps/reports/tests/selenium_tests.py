from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase


class TestSelenium(QiConservativeSeleniumTestCase):
    selenium_fixtures = []
    



    def test_all_pages_load(self):
        sel = self.selenium
        sel.open("/people/search")
        sel.click("link=Reports")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Thursday Volunteer List")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("thursday night volunteers")
        self.assertEqual("Add new criteria", sel.get_text("link=Add new criteria"))
        sel.click("link=Reports")
        sel.wait_for_page_to_load("30000")
        sel.click("link=New Report")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Save Report", sel.get_text("link=Save Report"))
