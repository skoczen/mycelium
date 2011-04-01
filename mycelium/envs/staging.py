from base import *
ENV = "LIVE"
ROLE = "STAGING"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mycelium',
        'USER': 'root',
        'PASSWORD': 'pK9Xvt5Kv2dSH586cRrgJ',        
        'HOST': 'int-mysql.digitalmycelium.com',
        'PORT': '3306',
    },
}



MEDIA_URL = 'http://media.digitalmycelium.com/'
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
AWS_ACCESS_KEY_ID = 'AKIAJTNZWCZDOIDWFR4A'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = "goodcloud-staging"
AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
CDN_MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME

# django-mediasync
MEDIASYNC['AWS_BUCKET'] = AWS_STORAGE_BUCKET_NAME
MEDIA_URL = CDN_MEDIA_URL
STATIC_URL = MEDIA_URL
STATIC_ROOT = MEDIA_ROOT
