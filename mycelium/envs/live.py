from base import *
SSL_FORCE = True
# SESSION_COOKIE_SECURE = False
# SESSION_COOKIE_DOMAIN = "agoodcloud.com"
ENV = "LIVE"
ROLE = ENV

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mycelium',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    },
}

MIDDLEWARE_CLASSES += (
    'sslify.middleware.SSLifyMiddleware',
)

# DATABASE_ROUTERS = ['balancer.routers.PinningWMSRouter']

# DATABASE_POOL = {
#     'default': 1,
#     'slave': 1,
# }
MASTER_DATABASE = 'default'
BASE_DOMAIN = "agoodcloud.com"

# Stripe
STRIPE_SECRET = "xCtqHMmMyKlEMjbeiFgnoVYO72b6stA8"
STRIPE_PUBLISHABLE = "pk_oKB20RwO4kJ5jvsnDlSrw2E43YnbR"

MEDIA_URL = 'https://media.agoodcloud.com/'
MANUAL_MEDIA_URL = 'https://www.agoodcloud.com/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "/admin-media/"

# BROKER_BACKEND = "redis"
# BROKER_HOST = "drum.redistogo.com"  # Maps to redis host.
# BROKER_PORT = 9017         # Maps to redis port.
# REDIS_PORT = 9017
# BROKER_VHOST = "0"         # Maps to database number.
# CELERY_RESULT_BACKEND = "redis"
# REDIS_HOST = "drum.redistogo.com"

BROKER_URL = "redis://redistogo:b8b35d6f28e598ab6f56dca217c015d5@drum.redistogo.com:9017/0"  # Maps to redis host.
BROKER_HOST = BROKER_URL
CELERY_RESULT_BACKEND = None

BROKER_VHOST = "0"                       # Maps to database number.
REDIS_HOST = BROKER_HOST
REDIS_DB = BROKER_VHOST


CACHES = {
    # 'default': {
    #     'BACKEND' : 'johnny.backends.memcached.MemcachedCache',
    #     # 'LOCATION': 'int-Memcached1010.agoodcloud.com:11211',
    #     'LOCATION': 'mc10.ec2.northscale.net:11211',
    #     'USERNAME': "app1932005\%40heroku.com",
    #     'PASSWORD': "GWbcmVAj+AAm3sAB",
    #     'PREFIX':ENV,
    #     'JOHNNY_CACHE':True,
    # }
    'default': {
          'BACKEND': 'django_pylibmc.memcached.PyLibMCCache'
    #     'BACKEND': 'johnny.backends.memcached.PyLibMCCache',
        'PREFIX':ENV,
        'JOHNNY_CACHE':True,
    }
}

# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
# CACHE_BACKEND = 'johnny.backends.memcached://127.0.0.1:11211'

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_STORAGE_BUCKET_NAME = "goodcloud1"
AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME

STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
COMPRESS_URL = STATIC_URL

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = "lib.backends.CachedS3BotoStorage"
COMPRESS_STORAGE = STATICFILES_STORAGE

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

FAVICON_URL = "%simages/favicon.png" % STATIC_URL

