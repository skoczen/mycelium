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

    url(r'smart_group/new$',                                         views.new_smart_group,                         name='new_smart_group'),    
    url(r'smart_group/{smart_group_id:digits}$',                     views.smart_group,                             name='smart_group'),
    url(r'smart_group/delete$',                                      views.delete_smart_group,                      name='delete_smart_group'),    
)
