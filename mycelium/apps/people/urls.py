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
    url(r'person/save$',                                                    views.person_save,                                    name='person_save'),
    url(r'person/new$',                                                     views.person_new,                                     name='person_new'),
    url(r'person/delete$',                                                  views.person_delete,                                  name='person_delete'),
    url(r'person/phone_number/save$',                                       views.phone_number_save,                              name='phone_number_save'),
    url(r'person/phone_number/new$',                                        views.phone_number_new,                               name='phone_number_new'),
    url(r'person/phone_number/delete$',                                     views.phone_number_delete,                            name='phone_number_delete'),
    url(r'person/email/save$',                                              views.email_save,                                     name='email_save'),
    url(r'person/email/new$',                                               views.email_new,                                      name='email_new'),
    url(r'person/email/delete$',                                            views.email_delete,                                   name='email_delete'),
    url(r'person/employee/save$',                                           views.employee_save,                                  name='employee_save'),
    url(r'person/employee/new$',                                            views.employee_new,                                   name='employee_new'),
    url(r'person/employee/delete$',                                         views.employee_delete,                                name='employee_delete'),
    
)