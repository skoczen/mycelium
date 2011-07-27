from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^webhooks/',     include('webhooks.urls',            app_name="webhooks",        namespace="webhooks")),
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
