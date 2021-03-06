# encoding: utf-8
import time
from test_factory import Factory
from django.core.cache import cache

def _sitespaced_url(url, site="test"):
    from django.conf import settings
    spacer = ""
    if site != "":
        spacer = "."
    return "http://%s%slocalhost:%s%s" % (site, spacer, settings.LIVE_SERVER_PORT, url)

class AccountTestAbstractions(object):
    MANAGE_USERS_URL = "/accounts/manage-users"
    
    def create_demo_site(self, name="test", mostly_empty=False, **kwargs):
        return Factory.create_demo_site(name, quick=True, delete_existing=True,  mostly_empty=mostly_empty, create_subscription=True, **kwargs)

    def go_to_the_login_page(self, site=None):
        sel = self.selenium
        self.open("/login", site=site)
        sel.wait_for_page_to_load("30000")

    def log_in(self, ua=None, with_assert=True, username=None, password=None):
        sel = self.selenium
        if not username:
            if not ua:
                username = "admin"
            else:
                username = ua.denamespaced_username
        if not password:
            password = username
        
        sel.type("css=input[name=username]",username)
        sel.type("css=input[name=password]",password)
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

    def open(self, url, site=None):
        if not site:
            if hasattr(self,"site") and self.site:
                site = self.site
            else:
                site = "test"
        sel = self.selenium
        sel.open(_sitespaced_url(url, site=site))
        sel.wait_for_page_to_load("30000")

    def set_site(self, site):
        self.site = site

    def get_logged_in(self, name="test"):
        self.go_to_the_login_page(site=name)
        self.log_in()
        self.assert_login_succeeded()

    def setup_for_logged_in(self, name="test", mostly_empty=False, **kwargs):
        cache.clear()
        self.account = self.create_demo_site(name=name, mostly_empty=mostly_empty, **kwargs)
        self.go_to_the_login_page(site=name)
        self.log_in()

        self.assert_login_succeeded()
        return self.account

    def setup_for_logged_in_with_no_data(self, name="test", mostly_empty=True, single_user=True):
        return self.setup_for_logged_in(name=name, mostly_empty=mostly_empty, single_user=single_user)


    def go_to_the_manage_accounts_page(self):
        sel = self.selenium
        sel.click("css=.admin_btn")
        sel.wait_for_page_to_load("30000")
        sel.click("css=.users_button")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Account Level")

    def go_to_the_account_page(self):
        sel = self.selenium
        sel.click("css=.admin_btn")
        sel.wait_for_page_to_load("30000")
        sel.click("css=.account_button")
        sel.wait_for_page_to_load("30000")
        # time.sleep(60)
        assert sel.is_text_present("Account Information")


    def create_a_new_user_via_manage_accounts(self, full_name="Joe Smith", username="jsmith", password="test", access_level=0):
        sel = self.selenium
        self.go_to_the_manage_accounts_page()
        sel.click("css=tab_title")
        time.sleep(0.5)
        sel.type("css=#id_first_name", full_name)
        sel.type("css=#id_username", username)
        sel.type("css=#id_password", password)
        sel.type("css=#id_email", "test_%s@example.com" % username)
        sel.click("css=#id_access_level_%s" % access_level)
        time.sleep(0.5)
        sel.click("css=.create_account_btn")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present(full_name)
        assert sel.is_text_present(username)
        assert sel.is_text_present(password)


    def go_to_my_account_page(self):
        sel = self.selenium
        sel.click("css=.admin_btn")
        sel.wait_for_page_to_load("30000")
        sel.click("css=.my_account_button")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("My Account")

    def get_my_full_name(self):
        sel = self.selenium
        sel.click("css=.my_account_btn")
        sel.wait_for_page_to_load("30000")
        return sel.get_text("css=#container_id_first_name .view_field")

    def enter_billing_info_signup(self, valid_cc=True, cc_number=None):
        """Assumes you're starting on the manage acct page"""
        if not cc_number:
            cc_number = Factory.test_cc_number(valid_cc)

        sel = self.selenium
        sel.click("link=Update Billing Information")
        sel.type("css=#id_card_number",cc_number)
        sel.type("css=#id_card_cvv","123")
        sel.select("css=#id_card_expiry_month","May")
        sel.select("css=#id_card_expiry_year","2020")

        sel.click("css=#subscription_submit")
        if valid_cc:
            sel.wait_for_page_to_load("30000")
        else:
            time.sleep(6)
