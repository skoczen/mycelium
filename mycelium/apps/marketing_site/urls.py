from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'^',                    views.home,             name='home'),
    url(r'^about-us$',           views.about_us,         name='about_us'),
    url(r'^features$',           views.features,         name='features'),
    url(r'^tour$',               views.tour,             name='tour'),
    url(r'^praise$',             views.praise,           name='praise'),
    url(r'^legal$',              views.legal,            name='legal'),
    url(r'^contact_us$',         views.contact_us,       name='contact_us'),

    # Temp for SSL
    url(r'^d8GdULy.html$',       views.ssl_page,         name='ssl_page'),    
)