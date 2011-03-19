from base import *
ENV = "LIVE"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mycelium',
        'USER': 'root',
        'PASSWORD': 'Q3lg8Af81tj6vr5PdcIs',        
        'HOST': 'int-mysql.agoodcloud.com',
        'PORT': '3306',
    },
}

MEDIA_URL = 'https://media.agoodcloud.com/'
DJANGO_STATIC_MEDIA_URL = 'https://media.agoodcloud.com'
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
EMAIL_BACKEND = 'django_ses.SESBackend'

CDN_MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME