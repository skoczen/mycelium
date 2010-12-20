from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'search$',                           views.search,       name='search'),
    url(r'person/{person_id:digits}$',        views.person,       name='person'),
)