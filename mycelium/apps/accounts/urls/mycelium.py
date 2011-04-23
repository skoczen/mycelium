from django.conf.urls.defaults import *
from django.conf import settings
from accounts.forms import AccountAuthenticationForm
from accounts.views import mycelium as views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
   url(r'^login/$',                     views.login,              {'template_name': 'accounts/login.html', 
                                                                   'authentication_form':AccountAuthenticationForm,}     
                                                                                                                             , name="login"         ),
   url(r'^logged-out/$',               'django.contrib.auth.views.logout',      {'template_name': 'accounts/logout.html'}    , name="logout"        ),
)
