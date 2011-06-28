from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'{person_id:digits}/save-new-conversation$',                  views.save_new_conversation,                        name='save_new_conversation'),
    url(r'{conversation_id:digits}/delete-conversation$',              views.delete_conversation_from_people_tab,          name='delete_conversation_from_people_tab'),
)
