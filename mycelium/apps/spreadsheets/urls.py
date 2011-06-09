from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    # for testing
    url(r'report/1$',                       views.detail_volunteer,                    name='report_detail_volunteer'),
    url(r'report/2$',                       views.detail_donors,                       name='report_detail_donors'),
    url(r'report/3$',                       views.detail_email,                        name='report_detail_email'),


    url(r'$',                               views.search,                              name='search'),
    url(r'report/{report_id:digits}$',      views.detail,                              name='report_detail'),
    url(r'report/new$',                     views.new,    kwargs={'report_id':"new"},  name='new_report'),
    
)