# encoding: utf-8
import time
from django.core.cache import cache

class RewriteTestAbstractions(object):

    def get_to_management_console(self):
        sel = self.selenium
        sel.open("")
        
