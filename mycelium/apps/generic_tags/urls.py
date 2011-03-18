from django.conf.urls.defaults import *
from django.conf import settings

import dselector
parser = dselector.Parser()
url = parser.url

def tag_urls(view_class, prefix=""):
	return parser.patterns('',                      
    url(r'%sadd-tag$' % prefix,                                      		view_class.add_tag,                                  name='%sadd_tag' % view_class.namespace_name),
    url(r'%s{target_id:digits}/remove-tag$' % prefix,                		view_class.remove_tag,                               name='%sremove_tag' % view_class.namespace_name),
    url(r'%snew-tag-results$' % prefix,                              		view_class.new_tag_search_results,                   name='%snew_tag_search_results' % view_class.namespace_name),
	)
