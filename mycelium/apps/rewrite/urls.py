from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('django.views.generic.simple',                      
  (r'^tests/test0.html$',             'direct_to_template', {'template': 'rewrite/demo0.html'}),
  (r'^tests/test1.html$',             'direct_to_template', {'template': 'rewrite/demo1.html'}),
  (r'^tests/test2.html$',             'direct_to_template', {'template': 'rewrite/demo2.html'}),
  (r'^tests/test3.html$',             'direct_to_template', {'template': 'rewrite/demo3.html'}),
  (r'^tests/test4.html$',             'direct_to_template', {'template': 'rewrite/demo4.html'}),    
)