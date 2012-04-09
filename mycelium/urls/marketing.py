from django.conf.urls.defaults import *
import sys
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

# from django.template.loader import add_to_builtins
# add_to_builtins('django.templatetags.staticfiles')

urlpatterns = patterns('',

    url(r'^',              include('marketing_site.urls',      app_name="marketing_site",  namespace="marketing_site"),),
    url(r'^',              include('email_list.urls',          app_name="email_list",      namespace="email_list")),                                    
    url(r'^',              include('accounts.urls.marketing',  app_name="accounts",        namespace="accounts")),    

    url(r'^blog/$', 'django.views.generic.simple.redirect_to', {'url': "http://goodcloud.posterous.com"}, 'blog'),
    url(r'^administration/', include(admin.site.urls)),
    # url(r'^webhooks/',     include('webhooks.urls',            app_name="webhooks",        namespace="webhooks")),
    url(r'^zebra/',        include('zebra.urls',               app_name="zebra",           namespace="zebra")),
    
    url(r'^', include('django_ses.urls')),
)

if settings.DEBUG or settings.SELENIUM_TESTING:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += staticfiles_urlpatterns()


if "compress" in sys.argv:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )

# override for qi urls to allow indexing
from qi_toolkit import robots
urlpatterns += patterns('',          
    url(r'^robots.txt',     robots.robots_txt,      kwargs={'allow':True,},    name='robots_txt'),
)

try:
    if settings.FAVICON_URL != "":
        urlpatterns += patterns('',          
            (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': settings.FAVICON_URL}),
        )
except:
    pass
