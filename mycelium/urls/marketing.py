from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from django.template import add_to_builtins
add_to_builtins('mediasync.templatetags.media')

urlpatterns = patterns('',

    (r'^',              include('marketing_site.urls',      app_name="marketing_site",  namespace="marketing_site"),),
    (r'^',              include('email_list.urls')),                                    
    (r'^accounts/',     include('accounts.urls',            app_name="accounts",        namespace="accounts")),    
    
    (r'^blog/$', 'django.views.generic.simple.redirect_to', {'url': "http://goodcloud.posterous.com"}, 'blog_home'),
    (r'^admin/', include(admin.site.urls)),
    (r'^', include('sorl.thumbnail.urls')),
    url(r'^', include('qi_toolkit.urls')),
    url(r'^', include('cms.urls')),
    url(r'^', include('django_ses.urls')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^', include('mediasync.urls')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
