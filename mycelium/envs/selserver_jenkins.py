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

# turn on to test pre-deploy
MEDIASYNC['EMULATE_COMBO'] = True
SOUTH_TESTS_MIGRATE = False
