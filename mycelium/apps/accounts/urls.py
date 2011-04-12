from django.conf.urls.defaults import *
from django.conf import settings
from groups import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    # url(r'group/new$',                                               views.new_group,                               name='new_group'),    
   
)
