from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'$',                               views.search,                              name='search'),
    url(r'report/{report_id:digits}$',      views.detail,                              name='report_detail'),
    url(r'report/new$',                     views.detail, kwargs={'report_id':"new"},  name='new_report'),
)