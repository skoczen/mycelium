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
    url(r'organization/new$',                                               views.new_organization,                               name='new_organization'),    
    url(r'organization/{org_id:digits}$',                                   views.organization,                                   name='organization'),
    url(r'organization/delete$',                                            views.delete_organization,                            name='delete_organization'),    
    url(r'organization/{org_id:digits}/save-basic$',                        views.save_organization_basic_info,                   name='organization_save_basic'),
    url(r'organization/{org_id:digits}/save-employees$',                    views.save_organization_employees,                    name='organization_save_employees'),    
    url(r'organization/{org_id:digits}/remove-employee/{emp_id:digits}/$',  views.remove_employee,                                name='organization_remove_employee'),        
    url(r'organization/{org_id:digits}/new-person$',                        views.new_person_via_organization,                    name='new_person_via_organization'),
    url(r'organization/{org_id:digits}/existing-person$',                   views.existing_person_via_organization,               name='existing_person_via_organization'),    
    url(r'organization/new-person/search-results$',                         views.add_person_via_organization_search_results,     name='add_person_via_organization_search_results'), 

    url(r'person/add-tag$',                                                 views.add_person_tag,                                 name='add_person_tag'),
    url(r'person/{person_id:digits}/remove-tag$',                           views.remove_person_tag,                              name='remove_person_tag'),
    url(r'person/new-tag-results$',                                         views.new_tag_search_results,                         name='new_tag_search_results'),
    
    url(r'organization/add-tag$',                                           views.add_organization_tag,                           name='add_organization_tag'),
    url(r'organization/{org_id:digits}/remove-tag$',                        views.remove_organization_tag,                        name='remove_organization_tag'),
)