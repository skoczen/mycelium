from django.conf.urls.defaults import *
from django.conf import settings
from rewrite.views import private as views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
   # Redirect to dashboard
    # url(r'^$',                                           views.dashboard                                                                      , name="dashboard"                 ),
)
