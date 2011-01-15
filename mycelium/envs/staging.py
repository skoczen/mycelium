from base import *

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',
        'NAME': 'skoczen_mycelium_staging',
        'USER': 'skoczen_mycelium_staging',
        'PASSWORD': 'ba21794b',
        'HOST': 'web58.webfaction.com',
        'PORT': '',
    },
}
ENV = "STAGING"

MEDIA_URL = 'http://testing.agoodcloud.com/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)
