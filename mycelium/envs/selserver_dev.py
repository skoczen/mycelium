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
}

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SELENIUM_TESTING = True
BASE_DOMAIN = "localhost:8099"
# CACHE_BACKEND = 'locmem://'
# CELERY_ALWAYS_EAGER = True




BROKER_VHOST = "3"                       # Maps to database number.
CACHES['default']['PREFIX'] = "%s-selenium"
