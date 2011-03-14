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
DJANGO_STATIC = True
