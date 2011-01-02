from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),


    (r'^', include('marketing_site.urls', app_name="marketing_site", namespace="marketing_site"),),
    (r'^', include('email_list.urls')),    
    (r'^', include('rewrite.urls')),        
    (r'^people/', include('people.urls', app_name="people", namespace="people")),
    (r'^reports/', include('reports.urls', app_name="reports", namespace="reports")),
    
    (r'^blog/$', 'django.views.generic.simple.redirect_to', {'url': "http://goodrain.agoodcloud.com"}, 'blog_home'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),    
)
