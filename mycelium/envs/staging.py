from base import *
ENV = "LIVE"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mycelium',
        'USER': 'root',
        'PASSWORD': 'pK9Xvt5Kv2dSH586cRrgJ',        
        'HOST': 'int-mysql.staging.digitalmycelium.com',
        'PORT': '3306',
    },
}

MEDIA_URL = 'http://staging.digitalmycelium.com/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
FAVICON_URL = "%simages/favicon.png" % MEDIA_URL

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'PREFIX':ENV
    }
}

CACHE_BACKEND = 'memcached://127.0.0.1:11211/'