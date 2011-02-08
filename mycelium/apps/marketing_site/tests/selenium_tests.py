from djangosanetesting.cases import SeleniumTestCase
from email_list.models import EmailSubscription

class TestMarketingSite(SeleniumTestCase):
    selenium_fixtures = ["marketing_site.json",]
    # fixtures = ["marketing_site.json",]

    def setUp(self):
        self.verificationErrors = []
    
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    def test_home_page_loads(self):
        sel = self.selenium
        sel.open("/")


    def test_each_page_loads(self):
        sel = self.selenium
        sel.open("/")
        sel.click("link=Home")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Mission")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("We get nonprofits.", sel.get_text("//div[@id='page_content']/h2[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Nonprofits deserve the best software in the world.", sel.get_text("//div[@id='page_content']/h1"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("All content copyright GoodCloud, LLC, 2010-2011", sel.get_text("//div[@id='footer']/div[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=About Us")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Steven Skoczen", sel.get_text("//div[@id='page_content']/div/div[1]/div[2]/div[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Tom Noble", sel.get_text("//div[@id='page_content']/div/div[2]/div[2]/div[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Contact")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("support@agoodcloud.org", sel.get_text("link=support@agoodcloud.org"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Give us a call at (503) 308-1460", sel.get_text("//div[@id='page_content']/p[3]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=Home")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Welcome to GoodCloud.", sel.get_text("//td[@id='home_right_content']/p[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))

        
        
    def test_users_can_submit_their_emails(self):
        sel = self.selenium
        sel.open("/")
        sel.click("link=Home")
        sel.wait_for_page_to_load("30000")
        sel.type("id_email", "myemail@me.com")
        try: self.assertEqual("Save Email", sel.get_value("id_submit"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_email")
        try: self.assertEqual("We hate spam, too. We'll only use your email to notify you of updates.", sel.get_text("//td[@id='home_right_content']/div[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("id_submit")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Thanks! We'll keep you posted!", sel.get_text("//td[@id='home_right_content']/div[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        email_sub = EmailSubscription.objects.filter(email="myemail@me.com")
        assert email_sub.count() == 1