from django.conf.urls.defaults import *
from django.conf import settings
from webhooks import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'^chargify/postback$',                 views.chargify_postback,                         name="chargify_postback"),
    url(r'^chargify/webhook$',                  views.chargify_webhook,                          name="chargify_webhook"),
)
