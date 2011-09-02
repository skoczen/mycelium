# encoding: utf-8
import time
from django.core.cache import cache
from django.core.urlresolvers import reverse

class RewriteTestAbstractions(object):

    def _private_urlify(self, url):
        return "http://localhost:8000/%s" % url
    
    def _open_private_url(self, url):
        sel = self.selenium
        sel.open(self._private_urlify())
        sel.wait_for_page_to_load("30000")

    def get_to_management_console(self):
        self._open_private_url(reverse("rewrite:manage_home"))

    
    def assert_in_the_management_console(self):
        sel = self.selenium
        assert sel.is_text_present("Website Manager")
        
