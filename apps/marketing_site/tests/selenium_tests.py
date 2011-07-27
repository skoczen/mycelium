import time
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase, QiSeleniumTestCase
from email_list.models import EmailSubscription

class TestMarketingSite(QiSeleniumTestCase):
    # selenium_fixtures = ["marketing_site_localhost.json"]
    # fixtures = ["marketing_site.json",]

    def setUp(self):
        from django.contrib.sites.models import Site
        s = Site.objects.get(pk=1)
        s.id = 2
        s.domain = "localhost"
        s.name = "localhost"
        s.save()


    def test_each_page_loads(self):
        sel = self.selenium
        sel.open("/")
        
        # Home
        sel.click("css=#logo")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Built for Small Nonprofits")

        # Features
        sel.click("link=Our Mission")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Do Good Things.")

        sel.click("link=Features")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("All the things you actually need.")

        # Tour
        sel.click("link=Tour")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Watch it in action")

        # Pricing
        sel.click("link=Pricing")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("We like to keep things simple.")


        # Free Trial
        sel.click("link=Sign Up")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("One-step easy.")
        
        # About Us
        sel.click("link=About Us")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Small nonprofits deserve the best software in the world.")

        # News /  Blog / Press
        sel.click("link=News")
        time.sleep(3)
        assert sel.is_text_present("All the latest news, and a couple great recipes.")
        sel.click("css=.issue_2011_07")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("July 2011")
        assert sel.is_text_present("Don't Let Your Nonprofit's")

        # Mission / About us
        sel.click("link=Our Team")
        time.sleep(3)
        assert sel.is_text_present("GoodCloud is currently a team of")

        # Legal
        sel.click("link=Legal")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("This document (the \"User Agreement\")")

        # Privacy Policy
        sel.click("link=Privacy Policy")
        time.sleep(3)
        assert sel.is_text_present("Information Gathering and Usage")

        # Contact us
        sel.click("link=Contact Us")
        time.sleep(3)
        assert sel.is_text_present("Say Hello!")
