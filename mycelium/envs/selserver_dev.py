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

# turn on to test pre-deploy
# MEDIASYNC['EMULATE_COMBO'] = True

# turn on to test postsync with live media
# MEDIASYNC['SERVE_REMOTE'] = True
# MEDIA_URL = CDN_MEDIA_URL

SITE_ID = 1