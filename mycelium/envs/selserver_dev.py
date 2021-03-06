from dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_mycelium',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    },
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_mycelium',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        'TEST_MIRROR': 'default'
    },
}
DATABASE_ROUTERS = ['balancer.routers.PinningWMSRouter']
DATABASE_POOL = {
  'default': 2,
  'slave': 1,
}
MASTER_DATABASE = 'default'


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SELENIUM_TESTING = True
BASE_DOMAIN = "localhost:8099"
# CACHE_BACKEND = 'locmem://'
# CELERY_ALWAYS_EAGER = True

# COMPRESS_ENABLED = True
# COMPRESS_URL = CDN_MEDIA_URL
# STATIC_URL = CDN_MEDIA_URL
SESSION_SAVE_EVERY_REQUEST = True


BROKER_VHOST = "3"                       # Maps to database number.
CACHES['default']['PREFIX'] = "%s-selenium"
