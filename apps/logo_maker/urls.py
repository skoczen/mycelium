from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'logos$',                                 views.list_logos,                       name='list_logos'),
    url(r'download-resized/{logo_id:digits}$',     views.download_resized,                 name='download_resized'),
)