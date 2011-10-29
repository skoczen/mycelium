from dev import *

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
DATABASE_ROUTERS = []

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SELENIUM_TESTING = True
BASE_DOMAIN = "localhost:8099"
# CACHE_BACKEND = 'locmem://'
# CELERY_ALWAYS_EAGER = True

COMPRESS_ENABLED = True
COMPRESS_URL = CDN_MEDIA_URL
STATIC_URL = CDN_MEDIA_URL



BROKER_VHOST = "3"                       # Maps to database number.
CACHES['default']['PREFIX'] = "%s-selenium"
