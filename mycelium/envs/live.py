from base import *
SSL_FORCE = True
SESSION_COOKIE_SECURE = True
ENV = "LIVE"
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
BASE_DOMAIN = "agoodcloud.com"

# Stripe
STRIPE_SECRET = "xCtqHMmMyKlEMjbeiFgnoVYO72b6stA8"
STRIPE_PUBLISHABLE = "pk_oKB20RwO4kJ5jvsnDlSrw2E43YnbR"

MEDIA_URL = 'http://media.agoodcloud.com/'
MANUAL_MEDIA_URL = 'http://www.agoodcloud.com/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "/admin-media/"



BROKER_HOST = "int-Redis.agoodcloud.com"  # Maps to redis host.
BROKER_VHOST = "0"                       # Maps to database number.
REDIS_HOST = BROKER_HOST
REDIS_DB = BROKER_VHOST


CACHES = {
    'default': {
        'BACKEND' : 'johnny.backends.memcached.MemcachedCache',
        'LOCATION': 'int-Memcached1010.agoodcloud.com:11211',
        'PREFIX':ENV,
        'JOHNNY_CACHE':True,
    }
}

# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
# CACHE_BACKEND = 'johnny.backends.memcached://127.0.0.1:11211'

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_STORAGE_BUCKET_NAME = "goodcloud1"
AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
CDN_MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME
COMPRESS_URL = CDN_MEDIA_URL
COMPRESS_ENABLED = True
# COMPRESS_OFFLINE = True

STATIC_URL = CDN_MEDIA_URL
# STATIC_ROOT = MEDIA_ROOT

FAVICON_URL = "%simages/favicon.png" % STATIC_URL

