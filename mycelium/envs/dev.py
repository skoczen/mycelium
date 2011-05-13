from base import *
ENV = "DEV"
ROLE = ENV
SITE_ID = 2

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
# use in-memory for tests
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mycelium',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',
        },
    }


CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
# if not 'test' in sys.argv and not 'selenium_tests' in sys.argv:
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         # 'BACKEND' : 'johnny.backends.memcached.MemcachedClass',
#         'LOCATION': '127.0.0.1:11211',
#         'PREFIX':ENV,
#         'JOHNNY_CACHE':True,

#     }
# }
#CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
CACHE_BACKEND = 'johnny.backends.memcached://127.0.0.1:11211'


BROKER_VHOST = "2"                       # Maps to database number.

# SESSION_COOKIE_DOMAIN = "localhost"
DEBUG = True
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = False
INTERNAL_IPS = ('127.0.0.1')
GOOGLE_KEY = 'ABQIAAAAHhU2Kv9Iz8Fh-GRXaplHqxRi_j0U6kJrkFvY4-OX2XYmEAa76BQkakI7eN4BbYehPxnhnOMnaAhOPw'

MEDIA_URL = '/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "%s/_admin/" % (MEDIA_URL)
FAVICON_URL = "%s/images/favicon.png" % MEDIA_URL

# selenium settings
# SELENIUM_BROWSER_COMMAND = "*safari"
VIRTUALENV_PATH = "~/.virtualenvs/mycelium"
SELENIUM_TEST_SERVER_SETTINGS="selserver_dev"
# FORCE_SELENIUM_TESTS = True


SOUTH_TESTS_MIGRATE = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_ACCESS_KEY_ID = 'AKIAJTNZWCZDOIDWFR4A'
# AWS_SECRET_ACCESS_KEY = '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'

# local file storage
# DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"

# s3 info
AWS_STORAGE_BUCKET_NAME = "goodcloud-dev"
AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
CDN_MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME


# django-mediasync
STATIC_ROOT = MEDIA_ROOT
MEDIASYNC['SERVE_REMOTE'] = False
MEDIASYNC['EMULATE_COMBO'] = False
MEDIASYNC['AWS_BUCKET'] = AWS_STORAGE_BUCKET_NAME

# turn on to test pre-deploy
# MEDIASYNC['EMULATE_COMBO'] = True

# turn on to test postsync with live media
# MEDIASYNC['SERVE_REMOTE'] = True
# MEDIA_URL = CDN_MEDIA_URL

