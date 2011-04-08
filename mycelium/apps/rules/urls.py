from django.conf.urls.defaults import *
from django.conf import settings
from rules import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'rules_logic\.js$',                                     views.rules_logic_js,                               name='rules_logic_js'),    
)
