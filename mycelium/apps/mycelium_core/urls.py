from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'more$',                           views.more_menu,                     name='more_menu'),
    url(r'always_500$',                     views.always_500,                    name='always_500'),
)