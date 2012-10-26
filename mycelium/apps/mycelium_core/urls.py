from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'more$',                           views.more_menu,                     name='more_menu'),
    url(r'global/search_results$',          views.search_results,                name='search_results'),
    
    url(r'always_500$',                     views.always_500,                    name='always_500'),
    url(r'always_502$',                     views.always_502,                    name='always_502'),    
    url(r'.*?crossdomain.xml',              views.crossdomain_xml,               name='crossdomain_xml'),    
)