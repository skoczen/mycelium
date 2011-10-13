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
# CACHE_BACKEND = 'locmem://'
# CELERY_ALWAYS_EAGER = True




BROKER_VHOST = "3"                       # Maps to database number.
CACHES['default']['PREFIX'] = "%s-selenium"

# turn on to test pre-deploy
# MEDIASYNC['EMULATE_COMBO'] = True

# turn on to test postsync with live media
# MEDIASYNC['SERVE_REMOTE'] = True
# MEDIA_URL = CDN_MEDIA_URL
