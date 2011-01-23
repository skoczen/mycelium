from djangosanetesting.cases import SeleniumTestCase

class TestSelenium(SeleniumTestCase):
    fixtures = ["marketing_site.json"]

    def test_home_page_loads(self):
        self.selenium.open("/")
