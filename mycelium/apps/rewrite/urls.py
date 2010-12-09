from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
  (r'^tests/test0.html$',             'django.views.generic.simple.direct_to_template', {'template': 'rewrite/demo0.html'}),
  (r'^tests/test1.html$',             'django.views.generic.simple.direct_to_template', {'template': 'rewrite/demo1.html'}),
  (r'^tests/test2.html$',             'django.views.generic.simple.direct_to_template', {'template': 'rewrite/demo2.html'}),
  (r'^tests/test3.html$',             'django.views.generic.simple.direct_to_template', {'template': 'rewrite/demo3.html'}),
  (r'^tests/test4.html$',             'django.views.generic.simple.direct_to_template', {'template': 'rewrite/demo4.html'}),    
)