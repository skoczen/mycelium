from django.conf.urls.defaults import *
from django.conf import settings
from flight_control import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'^$',                               views.home,                          name='home'),
    url(r'account/{account_id:digits}$',     views.account,                       name='account'),
    url(r'^search-results$',                 views.search_results,                name='search_results'),

)
