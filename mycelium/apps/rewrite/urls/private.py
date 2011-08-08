from django.conf.urls.defaults import *
from django.conf import settings
from rewrite.views import private as views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'$',               views.pages,            name="manage_home"         ),
    url(r'pages$',          views.pages,            name="manage_pages"        ),
    url(r'templates$',      views.templates,        name="manage_templates"    ),
    url(r'blog$',           views.blog,             name="manage_blog"         ),
    url(r'settings$',       views.settings,         name="manage_settings"     ),
)
