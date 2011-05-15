from base import *
SSL_FORCE = True
SESSION_COOKIE_SECURE = True
ENV = "STAGING"
ROLE = ENV


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mycelium',
        'USER': 'myceliumdb',
        'PASSWORD': 'Q3lg8Af81tj6vr5PdcIs',        
        'HOST': 'int-mysql-master.agoodcloud.com',
        'PORT': '3306',
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mycelium',
        'USER': 'myceliumdb',
        'PASSWORD': 'Q3lg8Af81tj6vr5PdcIs',        
        'HOST': 'int-mysql-slave.agoodcloud.com',
        'PORT': '3306',
    },
}

DATABASE_ROUTERS = ['balancer.routers.PinningWMSRouter']

DATABASE_POOL = {
    'default': 1,
    'slave': 1,
}
MASTER_DATABASE = 'default'

CDN_MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = 'http://media.agoodcloud.com/'
MEDIA_URL = CDN_MEDIA_URL
STATIC_URL = MEDIA_URL
STATIC_ROOT = MEDIA_ROOT

# ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
ADMIN_MEDIA_PREFIX = "/admin-media/"
FAVICON_URL = "%simages/favicon.png" % MEDIA_URL


BROKER_HOST = "int-Redis.agoodcloud.com"  # Maps to redis host.
BROKER_VHOST = "0"                       # Maps to database number.


# CACHES = {
#     'default': {
#         'BACKEND' : 'johnny.backends.memcached.MemcachedClass',
#         'LOCATION': '127.0.0.1:11211',
#         'PREFIX':ENV,
#         'JOHNNY_CACHE':True,
#     }
# }

# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
CACHE_BACKEND = 'johnny.backends.memcached://int-Memcached1010.agoodcloud.com:11211'

EMAIL_BACKEND = 'django_ses.SESBackend'
SESSION_COOKIE_DOMAIN = "agoodcloud.com"


# django-mediasync
MEDIASYNC['AWS_BUCKET'] = AWS_STORAGE_BUCKET_NAME
MEDIASYNC['USE_SSL'] = True
from git import Repo
try:
    GIT_CURRENT_SHA = Repo(PROJECT_ROOT).commit("%s_release" % ROLE.lower()).hexsha
except:
    GIT_CURRENT_SHA = Repo(PROJECT_ROOT).head.reference.commit.hexsha
MEDIASYNC["AWS_PREFIX"] = GIT_CURRENT_SHA
