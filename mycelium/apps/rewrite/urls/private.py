from django.conf.urls.defaults import *
from django.conf import settings
from rewrite.views import private as views

import dselector
parser = dselector.Parser()
url = parser.url

urlpatterns = parser.patterns('',                      
    url(r'$',                           views.pages,            name="manage_home"         ),
    url(r'pages$',                      views.pages,            name="manage_pages"        ),
    url(r'templates$',                  views.templates,        name="manage_templates"    ),
    url(r'blog$',                       views.blog,             name="manage_blog"         ),
    url(r'settings$',                   views.settings,         name="manage_settings"     ),
    url(r'save-page/{page_id:digits}$', views.save_page,        name="save_page"           ),
    url(r'save-post/{post_id:digits}$', views.save_post,        name="save_blog_post"      ),
    url(r'new-page$',                   views.new_page,         name="new_page"            ),
    url(r'new-section$',                views.new_section,      name="new_section"         ),
    url(r'new-template$',               views.new_template,     name="new_template"        ),
    url(r'new-blog-post$',              views.new_blog_post,    name="new_blog_post"       ),
)
