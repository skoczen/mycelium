from base import *
ENV = "STAGING"

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'skoczen_mycelium_staging',
        'USER': 'skoczen_mycelium_staging',
        'PASSWORD': 'ba21794b',
        'HOST': 'web58.webfaction.com',
        'PORT': '',
    },
}

MEDIA_URL = 'http://staging.agoodcloud.com/media/'
STATIC_ROOT = join(abspath(dirname(__file__)), "../../../../mycelium_staging_static")
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
FAVICON_URL = "%simages/favicon.png" % MEDIA_URL

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }