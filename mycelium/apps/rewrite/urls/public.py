from django.conf.urls.defaults import *
from django.conf import settings
from rewrite.views import public as views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
  url(r'^{section:slug}$',                         views.page,         name="section"),
  url(r'^{section:slug}/{page_name:slug}$',        views.page,         name="page"),
  url(r'^blog/$',                                  views.blog_home,    name="blog_home"),
  url(r'^blog/{entry_slug:slug}$',                 views.blog_entry,   name="blog_entry"),

  url(r'^tests/test0.html$',             'django.views.generic.simple.direct_to_template', {'template': 'rewrite/demo0.html'}),
  url(r'^tests/test1.html$',             'django.views.generic.simple.direct_to_template', {'template': 'rewrite/demo1.html'}),
  url(r'^tests/test2.html$',             'django.views.generic.simple.direct_to_template', {'template': 'rewrite/demo2.html'}),
  url(r'^tests/test3.html$',             'django.views.generic.simple.direct_to_template', {'template': 'rewrite/demo3.html'}),
  url(r'^tests/test4.html$',             'django.views.generic.simple.direct_to_template', {'template': 'rewrite/demo4.html'}),    
)
