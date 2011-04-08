from django.conf.urls.defaults import *
from django.conf import settings
from groups import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'group/new$',                                               views.new_group,                               name='new_group'),    
    url(r'group/{group_id:digits}$',                                 views.group,                                   name='group'),
    url(r'group/delete$',                                            views.delete_group,                            name='delete_group'),    
    url(r'group/{group_id:digits}/save-basic$',                      views.save_basic_info,                         name='save_basic_info'),
    url(r'group/{group_id:digits}/members-partial$',                 views.group_members_partial,                   name='group_members_partial'),
    
)
