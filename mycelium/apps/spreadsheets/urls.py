from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'$',                                                   views.search,                                   name='search'),
    url(r'search-results$',                                     views.search_results,                           name='search_results'),
    url(r'spreadsheet/{spreadsheet_id:digits}$',                views.spreadsheet,                              name='spreadsheet'),
    url(r'spreadsheet/download$',                               views.download,                                 name='download'),
    url(r'spreadsheet/{spreadsheet_id:digits}/save-basic$',     views.save_basic_info,                          name='save_basic_info'),
    url(r'spreadsheet/delete$',                                 views.delete,                                   name='delete'),

    url(r'new$',                                                views.new,                                      name='new_spreadsheet'),
    
    
)