from django.conf.urls.defaults import *

import dselector
parser = dselector.Parser()
url = parser.url

import views

urlpatterns = parser.patterns('',                      
    url(r'{tag_set_id:digits}/{target_id:digits}/create$',                  views.tag_views.create_tag,                          name='create_tag'),
    url(r'{tag_set_id:digits}/{tag_id:digits}/{target_id:digits}/add$',     views.tag_views.add_tag,                             name='add_tag'),
    url(r'{tag_set_id:digits}/{tag_id:digits}/{target_id:digits}/remove$',  views.tag_views.remove_tag,                          name='remove_tag'),    
    url(r'{tag_set_id:digits}/{target_id:digits}/search-results$',          views.tag_views.new_tag_search_results,              name='new_tag_search_results'),    
    url(r'new-tagset$',                                                     views.new_tagset,                                    name='new_tagset'),
    url(r'{tagset_id:digits}/new-tag$',                                     views.new_tag,                                       name='new_tag'),
    url(r'manage/$',                                                        views.manage,                                        name='manage'),
    url(r'save-tags-and-tagset/$',                                          views.save_tags_and_tagsets,                         name='save_tags_and_tagsets'),
    url(r'{tagset_id:digits}/delete-tagset$',                               views.delete_tagset,                                 name='delete_tagset'),
    url(r'{tag_id:digits}/delete-tag$',                                     views.delete_tag,                                    name='delete_tag'),
    
)