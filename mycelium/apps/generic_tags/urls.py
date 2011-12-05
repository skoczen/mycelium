import dselector

from django.conf.urls.defaults import *

from generic_tags.api import TagResource, TagSetResource
from generic_tags import views
 
parser = dselector.Parser()
url = parser.url

tagset_resource = TagSetResource()
tag_resource = TagResource()

urlpatterns = parser.patterns('',                      
    url(r'{tag_set_id:digits}/{target_id:digits}/create$',                  views.tag_views.create_tag,                          name='create_tag'),
    url(r'{tag_set_id:digits}/{tag_id:digits}/{target_id:digits}/add$',     views.tag_views.add_tag,                             name='add_tag'),
    url(r'{tag_set_id:digits}/{tag_id:digits}/{target_id:digits}/remove$',  views.tag_views.remove_tag,                          name='remove_tag'),    
    url(r'{tag_set_id:digits}/{target_id:digits}/search-results$',          views.tag_views.new_tag_search_results,              name='new_tag_search_results'),    
    url(r'new-tagset$',                                                     views.new_tagset,                                    name='new_tagset'),
    url(r'{tagset_id:digits}/new-tag$',                                     views.new_tag,                                       name='new_tag'),
    url(r'manage/$',                                                        views.manage,                                        name='manage'),
    url(r'save-tags-and-tagset/$',                                          views.save_tags_and_tagsets,                         name='save_tags_and_tagsets'),
    (r'api/', include(tagset_resource.urls)),
    (r'api/', include(tag_resource.urls)),
)