from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    # url(r'{volunteer_id:digits}/save-completed-shift$',           views.save_completed_volunteer_shift,                 name='save_completed_volunteer_shift'),    
)
