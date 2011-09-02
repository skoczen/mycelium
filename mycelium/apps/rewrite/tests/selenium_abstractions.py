# encoding: utf-8
import time
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template.defaultfilters import slugify

# TEMP
settings.LIVE_SERVER_PORT = 8000

class RewriteTestAbstractions(object):

    def _private_urlify(self, url):
        return "http://test.localhost:%s%s" % (settings.LIVE_SERVER_PORT, url)
    
    def _open_private_url(self, url):
        sel = self.selenium
        sel.open(self._private_urlify(url))
        sel.wait_for_page_to_load("30000")

    def _public_urlify(self, url):
        return "http://localhost:%s%s" % (settings.LIVE_SERVER_PORT, url)
    
    def _open_public_url(self, url):
        sel = self.selenium
        sel.open(self._public_urlify(url))
        sel.wait_for_page_to_load("30000")

    def get_to_management_console(self, username="admin", password="admin"):
        sel = self.selenium
        self._open_private_url(reverse("rewrite:manage_home"))
        if sel.is_element_present("css=input[value=Log In]") or sel.is_element_present("css=input[value=Log in]"):
            sel.type("css=input[name=username]",username)
            sel.type("css=input[name=password]",password)
            sel.click("css=input[type=submit]")
            sel.wait_for_page_to_load("30000")

    def open_page_publicly(self, name=None, section=None):
        if not name or not section:
            raise Exception, "Missing page name or section"
        else:
            return self._open_public_url(reverse("website:page", args=(slugify(section),slugify(name))))

    
    def assert_in_the_management_console(self):
        sel = self.selenium
        try:
            assert sel.is_text_present("Website Manager")
        except:
            time.sleep(60)
            raise Exception

    def get_to_manage_pages(self):
        self.get_to_management_console()

    def create_a_section(self, name="Section One"):
        sel = self.selenium
        self.get_to_manage_pages()
        sel.click("css=.new_section_link")
        sel.type("css=.new_section_form #id_name", name)
        sel.click("css=.new_section_form input[type=submit]")
        sel.wait_for_page_to_load("30000")
        assert sel.is_element_present("css=section")
        assert sel.is_text_present(name)


    def create_a_page(self, name="Test Page"):
        sel = self.selenium
        self.get_to_manage_pages()
        sel.click("css=.new_page_link")
        sel.type("css=.new_page_form #id_title", name)
        sel.click("css=.new_page_form input[type=submit]")