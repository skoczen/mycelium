from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'{donor_id:digits}/save-new-donation$',		        views.save_new_donation,		                name='save_new_donation'),
	url(r'{donation_id:digits}/delete-donation$',     	  		views.delete_donation_from_people_tab,     		name='delete_donation_from_people_tab'),
)
from generic_tags.urls import tag_urls
urlpatterns += tag_urls(views.tag_views, "donor/", url_namespace="donor")