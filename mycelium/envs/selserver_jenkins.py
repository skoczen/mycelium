from dev import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_mycelium',
        'USER': 'root',
        'PASSWORD': 'Q3lg8Af81tj6vr5PdcIs',        
        'HOST': 'localhost',
        'PORT': '3306',
    },
}

# turn on to test pre-deploy
MEDIASYNC['EMULATE_COMBO'] = True
SOUTH_TESTS_MIGRATE = False
