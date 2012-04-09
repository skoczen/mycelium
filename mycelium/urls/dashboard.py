from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()
import sys

# from django.template.loader import add_to_builtins
# add_to_builtins('django.templatetags.staticfiles')

urlpatterns = patterns('',

    url(r'^',              include('flight_control.urls',      app_name="flight_control",  namespace="flight_control"),),

    url(r'^administration/', include(admin.site.urls)),
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
    url(r'^robots.txt',     robots.robots_txt,      kwargs={'allow':False,},    name='robots_txt'),
)

try:
    if settings.FAVICON_URL != "":
        urlpatterns += patterns('',          
            (r'^favicon\.ico$', 'django.views.generic.simple.redirect_to', {'url': settings.FAVICON_URL}),
        )
except:
    pass

