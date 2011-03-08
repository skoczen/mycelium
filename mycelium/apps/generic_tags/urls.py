from django.conf.urls.defaults import *
from django.conf import settings

import dselector
parser = dselector.Parser()
url = parser.url

def tag_urls(view_class, prefix=""):
	return parser.patterns('',                      
    url(r'%sadd-tag$' % prefix,                                      		view_class.add_tag,                                  name='add_tag'),
    url(r'%s{target_id:digits}/remove-tag$' % prefix,                		view_class.remove_tag,                               name='remove_tag'),
    url(r'%snew-tag-results$' % prefix,                              		view_class.new_tag_search_results,                   name='new_tag_search_results'),
	)
