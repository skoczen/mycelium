from base import *
ENV = "DEV"

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

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'PREFIX':ENV
    }
}


MEDIA_URL = '/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
FAVICON_URL = "%simages/favicon.png" % MEDIA_URL


from os.path import join, abspath
MEDIA_ROOT = join(abspath(PROJECT_ROOT),"../media")

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = False
INTERNAL_IPS = ('127.0.0.1')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
GOOGLE_KEY = 'ABQIAAAAHhU2Kv9Iz8Fh-GRXaplHqxRi_j0U6kJrkFvY4-OX2XYmEAa76BQkakI7eN4BbYehPxnhnOMnaAhOPw'