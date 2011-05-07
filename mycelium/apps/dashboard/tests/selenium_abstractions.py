# encoding: utf-8
import time
from test_factory import Factory

class DashboardTestAbstractions(object):
    
    def get_to_the_dashboard(self):
        sel = self.selenium
        self.open("/dashboard")
        sel.wait_for_page_to_load(30000)