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

class RewriteTestAbstractions(object):

    pass
        
       
