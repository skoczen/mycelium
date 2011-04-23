from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from django.template import add_to_builtins
add_to_builtins('mediasync.templatetags.media')

urlpatterns = patterns('',
    (r'^',              include('mycelium_core.urls',       app_name="core",            namespace="core")),    
    (r'^volunteers/',   include('volunteers.urls',          app_name="volunteers",      namespace="volunteers")),
    (r'^people/',       include('people.urls',              app_name="people",          namespace="people")),
    (r'^donors/',       include('donors.urls',              app_name="donors",          namespace="donors")),
    (r'^reports/',      include('reports.urls',             app_name="reports",         namespace="reports")),
    (r'^import/',       include('import.urls',              app_name="import",          namespace="import")),
    (r'^logo/',         include('logo_maker.urls',          app_name="logo_maker",      namespace="logo_maker")),
    (r'^groups/',       include('groups.urls',              app_name="groups",          namespace="groups")),
    (r'^tags/',         include('generic_tags.urls',        app_name="generic_tags",    namespace="generic_tags")),
    (r'^rules/',        include('rules.urls',               app_name="rules",           namespace="rules")),
    (r'^accounts/',     include('accounts.urls.mycelium',   app_name="accounts",        namespace="accounts")),    
    
    # (r'^administration/doc/', include('django.contrib.admindocs.urls')),
    # (r'^administration/', include(admin.site.urls)),
    (r'^', include('sorl.thumbnail.urls')),
    url(r'^', include('qi_toolkit.urls')),    
    url(r'^', include('django_ses.urls')),
    # url(r'^tinymce/', include('tinymce.urls')),
    url(r'^', include('mediasync.urls')),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
