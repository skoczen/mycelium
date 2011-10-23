from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

if settings.COMPRESS_VERSIONED_STATIC_TAG_BUILTIN:
    from django.template.loader import add_to_builtins
    add_to_builtins('compressor.templatetags.versioned_static')

urlpatterns = patterns('',

    url(r'^',              include('flight_control.urls',      app_name="flight_control",  namespace="flight_control"),),

    url(r'^administration/', include(admin.site.urls)),
    url(r'^sentry/', include('sentry.web.urls')),
)

if settings.DEBUG or settings.SELENIUM_TESTING:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += staticfiles_urlpatterns()


# override for qi urls to allow indexing
from qi_toolkit import robots
urlpatterns += patterns('',          
    url(r'^robots.txt',     robots.robots_txt,      kwargs={'allow':False,},    name='robots_txt'),
)

try:
    if settings.FAVICON_URL != "":
        urlpatterns += patterns('',          
            (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': settings.FAVICON_URL}),
        )
except:
    pass

