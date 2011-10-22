from dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_mycelium',
        'USER': 'root',
        'PASSWORD': '',        
        'HOST': 'localhost',
        'PORT': '3306',
    },
}


SOUTH_TESTS_MIGRATE = False
