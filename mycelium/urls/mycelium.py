from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

from django.template import add_to_builtins
add_to_builtins('mediasync.templatetags.media')

urlpatterns = patterns('',
    url(r'^',              include('mycelium_core.urls',       app_name="core",            namespace="core")),    
    url(r'^volunteers/',   include('volunteers.urls',          app_name="volunteers",      namespace="volunteers")),
    url(r'^people/',       include('people.urls',              app_name="people",          namespace="people")),
    url(r'^organizations/',include('organizations.urls',       app_name="organizations",   namespace="organizations")),
    url(r'^donors/',       include('donors.urls',              app_name="donors",          namespace="donors")),
    url(r'^conversations/',include('conversations.urls',       app_name="conversations",   namespace="conversations")),    
    url(r'^spreadsheets/', include('spreadsheets.urls',        app_name="spreadsheets",    namespace="spreadsheets")),
    url(r'^import/',       include('data_import.urls',         app_name="data_import",     namespace="data_import")),
    url(r'^logo/',         include('logo_maker.urls',          app_name="logo_maker",      namespace="logo_maker")),
    url(r'^groups/',       include('groups.urls',              app_name="groups",          namespace="groups")),
    url(r'^tags/',         include('generic_tags.urls',        app_name="generic_tags",    namespace="generic_tags")),
    url(r'^rules/',        include('rules.urls',               app_name="rules",           namespace="rules")),
    url(r'^',              include('accounts.urls.mycelium',   app_name="accounts",        namespace="accounts")),
    url(r'^dashboard/',    include('dashboard.urls',           app_name="dashboard",       namespace="dashboard")),
    url(r'^zebra/',        include('zebra.urls',               app_name="zebra",           namespace="zebra")),
    
    # (r'^administration/doc/', include('django.contrib.admindocs.urls')),
    # (r'^administration/', include(admin.site.urls)),
    url(r'^', include('qi_toolkit.urls')),    
    url(r'^', include('django_ses.urls')),
    url(r'^', include('mediasync.urls')),
    
)

if settings.DEBUG or settings.SELENIUM_TESTING:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
    urlpatterns += staticfiles_urlpatterns()
