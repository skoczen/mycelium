from base import *
SSL_FORCE = False
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


BASE_DOMAIN = "agoodcloud.com"

# Stripe
STRIPE_SECRET = "xCtqHMmMyKlEMjbeiFgnoVYO72b6stA8"
STRIPE_PUBLISHABLE = "pk_oKB20RwO4kJ5jvsnDlSrw2E43YnbR"

MEDIA_URL = 'https://media.agoodcloud.com/'
MANUAL_MEDIA_URL = 'https://www.agoodcloud.com/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "/admin-media/"


# BROKER_URL = "redis://redistogo:b8b35d6f28e598ab6f56dca217c015d5@drum.redistogo.com:9017/0"  # Maps to redis host.
BROKER_URL = os.environ.get('REDIS_BROKER_URL')
BROKER_HOST = BROKER_URL
CELERY_RESULT_BACKEND = None

BROKER_VHOST = "0"                       # Maps to database number.
REDIS_HOST = BROKER_HOST
REDIS_DB = BROKER_VHOST

CACHES = {
    'default': {
        'BACKEND': 'custom_cache_backend.PyLibMCCache',
        'PREFIX': ENV,
        'JOHNNY_CACHE': True,
    }
}

EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_STORAGE_BUCKET_NAME = "goodcloud1"
AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME

STATIC_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
COMPRESS_URL = STATIC_URL

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = "lib.backends.CachedS3BotoStorage"
COMPRESS_STORAGE = STATICFILES_STORAGE

COMPRESS_OFFLINE = True
COMPRESS_ENABLED = True

FAVICON_URL = "%simages/favicon.png" % STATIC_URL

