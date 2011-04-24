# encoding: utf-8
import time
from test_factory import Factory

def _sitespaced_url(url, site="test"):
    from django.conf import settings
    return "http://%s.localhost:%s%s" % (site, settings.LIVE_SERVER_PORT, url)

class AccountTestAbstractions(object):
    
    def create_demo_site(self, name="test", mostly_empty=False):
        return Factory.create_demo_site(name, quick=True, delete_existing=True, mostly_empty=mostly_empty)

    def go_to_the_login_page(self, site="test"):
        sel = self.selenium
        sel.open(_sitespaced_url("/login", site=site))
        sel.wait_for_page_to_load("30000")

    def log_in(self, ua=None, with_assert=True):
        sel = self.selenium
        if not ua:
            username = "admin"
        else:
            username = ua.denamespaced_username
        
        sel.type("css=input[name=username]",username)
        sel.type("css=input[name=password]",username)
        sel.click("css=.login_btn")
        sel.wait_for_page_to_load("30000")
        if with_assert:
            assert sel.is_text_present("Powered by")
    
    def open_window(self, url, name, site="test"):
        sel = self.selenium
        sel.open_window(_sitespaced_url(url, site=site), name)

    def assert_login_failed(self):
        sel = self.selenium
        assert sel.is_text_present("Your username and password didn't match")

    def assert_login_succeeded(self):
        sel = self.selenium
        assert sel.is_text_present("Powered by")

    def open(self, url, site="test"):
        sel = self.selenium
        sel.open(_sitespaced_url(url, site=site))
        sel.wait_for_page_to_load("30000")

    def setup_for_logged_in(self, name="test", mostly_empty=False):
        self.account = self.create_demo_site(name=name, mostly_empty=mostly_empty)
        self.go_to_the_login_page(site=name)
        self.log_in()
        self.assert_login_succeeded()
        return self.account

    def setup_for_logged_in_with_no_data(self, name="test", mostly_empty=True):
        return self.setup_for_logged_in(name=name, mostly_empty=mostly_empty)
