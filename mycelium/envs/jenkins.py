from live import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mycelium',
        'USER': 'root',
        'PASSWORD': '',        
        'HOST': 'localhost',
        'PORT': '3306',
    },
}


CACHE_BACKEND = 'locmem://'


MEDIA_URL = '/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
FAVICON_URL = "%simages/favicon.png" % STATIC_URL


SEND_BROKEN_LINK_EMAILS = False
INTERNAL_IPS = ('127.0.0.1')
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
GOOGLE_KEY = 'ABQIAAAAHhU2Kv9Iz8Fh-GRXaplHqxRi_j0U6kJrkFvY4-OX2XYmEAa76BQkakI7eN4BbYehPxnhnOMnaAhOPw'

SELENIUM_BROWSER_COMMAND = "*firefox"
VIRTUALENV_PATH = "/var/lib/jenkins/jobs/mycelium/workspace/ve"
SELENIUM_TEST_SERVER_SETTINGS="selserver_jenkins"
SOUTH_TESTS_MIGRATE = False