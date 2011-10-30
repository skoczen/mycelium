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
    'slave': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_mycelium',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
        'TEST_MIRROR': 'default'
    },
}
DATABASE_ROUTERS = ['balancer.routers.PinningWMSRouter']
DATABASE_POOL = {
  'default': 2,
  'slave': 1,
}
MASTER_DATABASE = 'default'

SOUTH_TESTS_MIGRATE = False
SESSION_SAVE_EVERY_REQUEST = True