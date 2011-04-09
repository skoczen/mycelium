from django.conf.urls.defaults import *

import dselector
parser = dselector.Parser()
url = parser.url

import views

urlpatterns = parser.patterns('',                      
    url(r'{tag_set_name:slug}/{target_id:digits}/add$',                     views.tag_views.add_tag,                             name='add_tag'),
    url(r'{tag_set_name:slug}/{target_id:digits}/remove$',                  views.tag_views.remove_tag,                          name='remove_tag'),    
    url(r'{tag_set_name:slug}/{target_id:digits}/search-results$',          views.tag_views.new_tag_search_results,              name='new_tag_search_results'),    
    url(r'{person_id:digits}/new-tagset$',                                  views.new_tagset,                                    name='new_tagset'),
    url(r'{tagset_id:digits}/rename-tagset$',                               views.rename_tagset,                                 name='rename_tagset'),
    url(r'{tagset_id:digits}/delete-tagset$',                               views.delete_tagset,                                 name='delete_tagset'),
    url(r'manage/$',                                                        views.manage,                                        name='manage'),
    
)