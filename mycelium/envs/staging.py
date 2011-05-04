from base import *
ENV = "LIVE"
ROLE = "STAGING"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mycelium',
        'USER': 'root',
        'PASSWORD': 'pK9Xvt5Kv2dSH586cRrgJ',        
        'HOST': 'int-mysql-staging-master.digitalmycelium.com',
        'PORT': '3306',
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mycelium',
        'USER': 'root',
        'PASSWORD': 'pK9Xvt5Kv2dSH586cRrgJ',        
        'HOST': 'int-mysql-staging-slave.digitalmycelium.com',
        'PORT': '3306',
    },
}
DATABASE_ROUTERS = ['envs.routers.MasterSlaveRouter',]


MEDIA_URL = 'http://media.digitalmycelium.com/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "/admin-media/"
FAVICON_URL = "%simages/favicon.png" % MEDIA_URL

# CACHES = {
#     'default': {
#         'BACKEND' : 'johnny.backends.memcached.MemcachedClass',
#         'LOCATION': '127.0.0.1:11211',
#         'PREFIX':ENV,
#         'JOHNNY_CACHE':True,
#     }
# }

# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
CACHE_BACKEND = 'johnny.backends.memcached://127.0.0.1:11211'

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_STORAGE_BUCKET_NAME = "goodcloud-staging"
AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
CDN_MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME

# django-mediasync
MEDIASYNC['AWS_BUCKET'] = AWS_STORAGE_BUCKET_NAME
MEDIA_URL = CDN_MEDIA_URL
STATIC_URL = MEDIA_URL
STATIC_ROOT = MEDIA_ROOT
SITE_ID = 3

