from django.conf.urls.defaults import *
from django.conf import settings
from groups import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    # url(r'group/new$',                                               views.new_group,                               name='new_group'),    
   url(r'^login/$',                                     'django.contrib.auth.views.login',       {'template_name': 'accounts/login.html'}     , name="login"        ),
   url(r'^logged-out/$',                                'django.contrib.auth.views.logout',      {'template_name': 'accounts/logout.html'}    , name="logout"        ),
)
