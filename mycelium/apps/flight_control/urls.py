from django.conf.urls.defaults import *
from django.conf import settings
from flight_control import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'^$',                                      views.home,                          name='home'),
    url(r'account/{account_id:digits}$',            views.account,                       name='account'),
    url(r'^search-results$',                        views.search_results,                name='search_results'),
    url(r'^account/{account_id:digits}/delete$',    views.delete_deactivated_account,    name="delete_deactivated_account"   ),
    url(r'^accounts/{ua_id:digits}/reset-password$',views.reset_account_password,        name="reset_account_password"    ),
)
