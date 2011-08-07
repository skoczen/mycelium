from django.conf.urls.defaults import *
from django.conf import settings
from rewrite.views import private as views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
   # Redirect to dashboard
    url(r'manage^$',                views.pages              , name="manage"       ),
    url(r'manage/pages^$',          views.pages              , name="pages"        ),
    url(r'manage/template^$',       views.template           , name="template"     ),
    url(r'manage/blog^$',           views.blog               , name="blog"         ),
    url(r'manage/settings^$',       views.settings           , name="settings"     ),
)
