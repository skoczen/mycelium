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
        try: self.assertEqual("Thursday Volunteer List", sel.get_text("css=.title"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Add new criteria", sel.get_text("link=Add new criteria"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Reports")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("New Report", sel.get_text("link=New Report"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Reports", sel.get_text("//div[@id='page']/div[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=New Report")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Unsaved Report", sel.get_text("css=.title"))
        except AssertionError, e: self.verificationErrors.append(str(e))