# encoding: utf-8
import time
from test_factory import Factory

class AccountTestAbstractions(object):
    def create_demo_site(self, name="test"):
        return Factory.create_demo_site(name,quick=True)

    def go_to_the_login_page(self, site="test"):
        from django.conf import settings
        sel = self.selenium
        sel.open("http://%s.localhost:%s" % (site,settings.LIVE_SERVER_PORT))
        sel.wait_for_page_to_load("30000")

    def log_in(self, ua=None):
        if not ua:
            username = "admin"
        else:
            username = ua.denamespaced_username
        sel = self.selenium
        sel.type("css=input[name=username]",username)
        sel.type("css=input[name=password]",username)
        sel.click("css=.login_btn")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Powered by")
    
    def assert_login_failed(self):
        sel = self.selenium
        assert sel.is_text_present("Your username and password didn't match")

    def assert_login_succeeded(self):
        sel = self.selenium
        assert sel.is_text_present("Powered by")

    def open(self, url, site="test"):
        from django.conf import settings
        sel = self.selenium
        sel.open("http://%s.localhost:%s%s" % (site,settings.LIVE_SERVER_PORT,url))
        sel.wait_for_page_to_load("30000")
