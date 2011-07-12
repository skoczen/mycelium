from django.conf.urls.defaults import *
from django.conf import settings
from accounts.forms import AccountAuthenticationForm
from accounts.views import marketing as views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'signup$',                             views.signup,                               name='signup'),    
    url(r'verify-subdomain$',                   views.verify_subdomain,                     name='verify_subdomain'),    

)
