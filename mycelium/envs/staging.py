from base import *
ENV = "STAGING"
ROLE = ENV
SITE_ID = 3

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mycelium',
        'USER': 'myceliumdb',
        'PASSWORD': 'pK9Xvt5Kv2dSH586cRrgJ',        
        'HOST': 'int-mysql-master.digitalmycelium.com',
        'PORT': '3306',
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mycelium',
        'USER': 'myceliumdb',
        'PASSWORD': 'pK9Xvt5Kv2dSH586cRrgJ',        
        'HOST': 'int-mysql-slave.digitalmycelium.com',
        'PORT': '3306',
    },
}
DATABASE_ROUTERS = ['balancer.routers.PinningWMSRouter']

DATABASE_POOL = {
    'default': 2,
    'slave': 1,
}
MASTER_DATABASE = 'default'


MEDIA_URL = 'http://media.digitalmycelium.com/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "/admin-media/"
FAVICON_URL = "%simages/favicon.png" % MEDIA_URL


BROKER_HOST = "int-Redis.digitalmycelium.com"  # Maps to redis host.
BROKER_VHOST = "1"                       # Maps to database number.
REDIS_HOST = BROKER_HOST


# CACHES = {
#     'default': {
#         'BACKEND' : 'johnny.backends.memcached.MemcachedClass',
#         'LOCATION': '127.0.0.1:11211',
#         'PREFIX':ENV,
#         'JOHNNY_CACHE':True,
#     }
# }

# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
# CACHE_BACKEND = 'johnny.backends.memcached://127.0.0.1:11211'
CACHE_BACKEND = 'johnny.backends.memcached://int-Memcached1010.digitalmycelium.com:11211'

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_STORAGE_BUCKET_NAME = "goodcloud-staging"
AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
CDN_MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME

# django-mediasync
MEDIASYNC['AWS_BUCKET'] = AWS_STORAGE_BUCKET_NAME
MEDIA_URL = CDN_MEDIA_URL
STATIC_URL = MEDIA_URL
STATIC_ROOT = MEDIA_ROOT


 
from git import Repo
try:
    GIT_CURRENT_SHA = Repo(PROJECT_ROOT).commit("%s_release" % ROLE.lower()).hexsha
except:
    GIT_CURRENT_SHA = Repo(PROJECT_ROOT).head.reference.commit.hexsha
MEDIASYNC["AWS_PREFIX"] = GIT_CURRENT_SHA
