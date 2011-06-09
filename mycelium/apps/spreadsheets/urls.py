from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    # for testing
    url(r'spreadsheet/1$',                       views.detail_volunteer,                    name='spreadsheet_detail_volunteer'),
    url(r'spreadsheet/2$',                       views.detail_donors,                       name='spreadsheet_detail_donors'),
    url(r'spreadsheet/3$',                       views.detail_email,                        name='spreadsheet_detail_email'),


    url(r'$',                               views.search,                              name='search'),
    url(r'spreadsheet/{spreadsheet_id:digits}$',      views.detail,                              name='spreadsheet_detail'),
    url(r'spreadsheet/new$',                     views.new,    kwargs={'spreadsheet_id':"new"},  name='new_spreadsheet'),
    
)