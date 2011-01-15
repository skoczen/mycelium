from base import *
from os.path import join, abspath

ENV = "DEV"
DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'mycelium',
        'USER': 'skoczen',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    },
}


DEBUG = True
TEMPLATE_DEBUG = DEBUG

SEND_BROKEN_LINK_EMAILS = False

MEDIA_URL = '/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
MEDIA_ROOT = join(abspath(PROJECT_ROOT),"../media")
FAVICON_URL = "%simages/favicon.png" % MEDIA_URL

ADMIN_MEDIA_PREFIX = '/media/admin/'


INTERNAL_IPS = ('127.0.0.1')
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
CACHE_BACKEND = 'dummy:///'
GOOGLE_KEY = 'ABQIAAAAHhU2Kv9Iz8Fh-GRXaplHqxRi_j0U6kJrkFvY4-OX2XYmEAa76BQkakI7eN4BbYehPxnhnOMnaAhOPw'

