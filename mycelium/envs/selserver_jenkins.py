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
DATABASE_ROUTERS = []

SOUTH_TESTS_MIGRATE = False
SESSION_SAVE_EVERY_REQUEST = True