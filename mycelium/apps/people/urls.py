from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'$',                                                               views.search,                                         name='search'),
    url(r'search$',                                                         views.search,                                         name='search_page'),
    url(r'search-results$',                                                 views.search_results,                                 name='search_results'),
    url(r'person/{person_id:digits}$',                                      views.person,                                         name='person'),
    url(r'person/{person_id:digits}/save-basic$',                           views.save_person_basic_info,                         name='person_save_basic'),
    url(r'person/new$',                                                     views.new_person,                                     name='new_person'),
    url(r'person/delete$',                                                  views.delete_person,                                  name='delete_person'),        
    url(r'person/{person_id:digits}/tab-contents$',                         views.tab_contents,                                   name='tab_contents'),
)