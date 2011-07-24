# encoding: utf-8
import time
from test_factory import Factory
from django.core.cache import cache
from django.contrib.auth.models import User
from django.conf import settings

class FlightControlTestAbstractions(object):

    def create_fake_account_for_flight_control(self):
        test_user = User.objects.create_user("admin", "test@example.com", "admin")
        test_user.is_active = True
        test_user.is_staff = True
        test_user.save()

    def get_to_flight_control(self):
        sel = self.selenium
        sel.open("http://flightcontrol.localhost:%s" % settings.LIVE_SERVER_PORT)
        sel.wait_for_page_to_load("30000")
        sel.type("css=#id_username", "admin")
        sel.type("css=#id_password", "admin")
        sel.click("css=input[type=submit]")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("GoodCloud Flight Control")
    
    def get_to_account_by_searching(self, name="test"):
        sel = self.selenium
        sel.type("css=#global_search", name)
        time.sleep(3)
        assert not sel.is_element_present("css=.no_people_found")
        assert sel.is_element_present("css=.results_found")
        sel.click("css=.results_found .striped_row a")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present(name)
        assert sel.is_text_present("Totals & Averages")