from base import *
ENV = "LIVE"

MEDIA_ROOT = abspath(STATIC_ROOT)
MEDIA_URL = 'http://www.agoodcloud.com/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
FAVICON_URL = "%simages/favicon.png" % MEDIA_URL

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',               # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'skoczen_mycelium',      # Or path to database file if using sqlite3.
        'USER': 'skoczen_mycelium',      # Not used with sqlite3.
        'PASSWORD': '5bc651ec',          # Not used with sqlite3.
        'HOST': 'web58.webfaction.com',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }