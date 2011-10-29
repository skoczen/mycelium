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
    # 'slave': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'mycelium',
    #     'USER': 'root',
    #     'PASSWORD': '',
    #     'HOST': 'localhost',
    #     'PORT': '',
    # },
}
#  DATABASE_ROUTERS = ['balancer.routers.PinningWMSRouter']
#  DATABASE_POOL = {
#    'default': 2,
#    'slave': 1,
#  }
#  MASTER_DATABASE = 'default'

# use in-memory for tests
# if 'test' in sys.argv:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.sqlite3',
#             'NAME': 'mycelium',
#             'USER': 'root',
#             'PASSWORD': '',
#             'HOST': 'localhost',
#             'PORT': '',
#         },
#     }

CELERY_ALWAYS_EAGER = False
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
# if not 'test' in sys.argv and not 'selenium_tests' in sys.argv:
CACHES = {
    'default': {
        'BACKEND' : 'johnny.backends.memcached.MemcachedCache',
        # 'BACKEND' : 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'PREFIX':ENV,
        'JOHNNY_CACHE':True,
    }
}

BROKER_VHOST = "2"                       # Maps to database number.

SESSION_COOKIE_DOMAIN = None
BASE_DOMAIN = "localhost:8000"
TIME_ZONE = "UTC"

DEBUG = True
TEMPLATE_DEBUG = DEBUG
SEND_BROKEN_LINK_EMAILS = False
INTERNAL_IPS = ('127.0.0.1')
GOOGLE_KEY = 'ABQIAAAAHhU2Kv9Iz8Fh-GRXaplHqxRi_j0U6kJrkFvY4-OX2XYmEAa76BQkakI7eN4BbYehPxnhnOMnaAhOPw'

MEDIA_URL = '/media/'
MANUAL_MEDIA_URL = MEDIA_URL
STATIC_URL =  '/static/'
ADMIN_MEDIA_PREFIX = "%s/_admin/" % (MEDIA_URL)


# selenium settings
# SELENIUM_BROWSER_COMMAND = "*safari"
VIRTUALENV_PATH = "~/.virtualenvs/mycelium"
SELENIUM_TEST_SERVER_SETTINGS="selserver_dev"
# FORCE_SELENIUM_TESTS = True
if 'selenium_tests' in sys.argv:
    BROKER_VHOST = "3"                       # Maps to database number.
    CACHES['default']['PREFIX'] = "%s-selenium"

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
COMPRESS_URL = STATIC_URL

# Comment this section to enable/disable testing.
# COMPRESS_ENABLED = True
# COMPRESS_URL = CDN_MEDIA_URL
# STATIC_URL = CDN_MEDIA_URL

FAVICON_URL = "%simages/favicon.png" % COMPRESS_URL


