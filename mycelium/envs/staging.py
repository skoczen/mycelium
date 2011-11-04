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
BASE_DOMAIN = "digitalmycelium.com"

# Stripe
STRIPE_SECRET = "vCqhGMFQvPOcg6EKKR2E28xX54PK3G3s"
STRIPE_PUBLISHABLE = "pk_DDh6nrKRl3zIvV0GTMaXr92c5dpKR"

MEDIA_URL = 'http://media.digitalmycelium.com/'
MANUAL_MEDIA_URL = 'http://digitalmycelium.com/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "/admin-media/"



BROKER_HOST = "int-Redis-staging.digitalmycelium.com"  # Maps to redis host.
BROKER_VHOST = "1"                       # Maps to database number.
REDIS_HOST = BROKER_HOST
REDIS_DB = BROKER_VHOST


CACHES = {
    'default': {
        'BACKEND' : 'johnny.backends.memcached.MemcachedCache',
        'LOCATION': 'int-Memcached1010.digitalmycelium.com:11211',
        'PREFIX':ENV,
        'JOHNNY_CACHE':True,
    }
}

# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
# CACHE_BACKEND = 'johnny.backends.memcached://127.0.0.1:11211'

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_STORAGE_BUCKET_NAME = "goodcloud-staging"
AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
CDN_MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME
COMPRESS_URL = CDN_MEDIA_URL
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

STATIC_URL = CDN_MEDIA_URL
# STATIC_ROOT = MEDIA_ROOT

FAVICON_URL = "%simages/favicon.png" % STATIC_URL

