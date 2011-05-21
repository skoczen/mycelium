from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'$',                                   views.list,                             name='list'),
    url(r'start/$',                             views.start,                            name='start'),
    url(r'history/{import_id:digits}$',         views.review,                           name='review'),

    url( r'start/upload/{import_type:word}/$',  views.data_import_uploader,             name="ajax_upload" ),
    url( r'columnHeaders.js$',                  views.import_column_headers_js,         name="import_column_headers_js" ),


)