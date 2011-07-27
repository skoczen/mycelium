from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      

    # url(r'^foo',                   views.do_signup,       name='email_do_signup'),
)