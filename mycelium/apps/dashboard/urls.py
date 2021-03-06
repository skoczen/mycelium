from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'^$',                               views.dashboard,                           name='dashboard'),
    url(r'save_nickname',                    views.save_nickname,                       name='save_nickname'),
    url(r'hide_challenge_complete_notice',   views.hide_challenge_complete_notice,      name='hide_challenge_complete_notice'),
    url(r'more_conversations',               views.more_conversations,                  name='more_conversations'),

)
