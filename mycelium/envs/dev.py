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
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'


# Use django-static
DJANGO_STATIC = False


MEDIA_URL = '/media/'
DJANGO_STATIC_MEDIA_URL = "/media"
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
FAVICON_URL = "%simages/favicon.png" % MEDIA_URL

# SELENIUM_BROWSER_COMMAND = "*safari"


DEBUG = True
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = False
INTERNAL_IPS = ('127.0.0.1')
GOOGLE_KEY = 'ABQIAAAAHhU2Kv9Iz8Fh-GRXaplHqxRi_j0U6kJrkFvY4-OX2XYmEAa76BQkakI7eN4BbYehPxnhnOMnaAhOPw'

SOUTH_TESTS_MIGRATE = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_ACCESS_KEY_ID = 'AKIAJTNZWCZDOIDWFR4A'
# AWS_SECRET_ACCESS_KEY = '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'

# DEFAULT_FILE_STORAGE = django.core.files.storage.FileSystemStorage
AWS_STORAGE_BUCKET_NAME = "goodcloud-dev"
AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
CDN_MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME
# MEDIA_URL = CDN_MEDIA_URL

# django-mediasync
STATIC_URL = MEDIA_URL
STATIC_ROOT = MEDIA_ROOT
MEDIASYNC['SERVE_REMOTE'] = False
MEDIASYNC['EMULATE_COMBO'] = True
MEDIASYNC['AWS_BUCKET'] = AWS_STORAGE_BUCKET_NAME


VIRTUALENV_PATH = "~/.virtualenvs/mycelium"
SELENIUM_TEST_SERVER_SETTINGS="selserver_dev"
FORCE_SELENIUM_TESTS = True