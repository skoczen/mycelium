from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'$',                                   views.list,                             name='list'),
    url(r'start/$',                             views.start,                            name='start'),
    url(r'history/{import_id:digits}$',         views.review,                           name='review'),
)