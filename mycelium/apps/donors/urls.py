from django.conf.urls.defaults import *
from django.conf import settings
import views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'{donor_id:digits}/save-new-donation$',		        views.save_new_donation,		                name='save_new_donation'),
	url(r'{donation_id:digits}/delete-donation$',     	  		views.delete_donation_from_people_tab,     		name='delete_donation_from_people_tab'),

    url(r'donor/add-tag$',                                                 views.add_donor_tag,                                  name='add_donor_tag'),
    url(r'donor/{donor_id:digits}/remove-tag$',                            views.remove_donor_tag,                               name='remove_donor_tag'),
    url(r'donor/new-tag-results$',                                         views.new_tag_search_results,                         name='new_tag_search_results'),

)
