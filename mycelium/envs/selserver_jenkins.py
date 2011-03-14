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

# Use django-static
DJANGO_STATIC = True
