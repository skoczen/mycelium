# Django settings for mycelium project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os, sys
from os.path import abspath, dirname, join
PROJECT_ROOT = join(abspath(dirname(__file__)), "../")
LIB_DIR = join(PROJECT_ROOT, 'lib')
APPS_DIR = join(PROJECT_ROOT, 'apps')
sys.path.insert(0, abspath(PROJECT_ROOT + '/../'))
sys.path.insert(0, LIB_DIR)
sys.path.insert(0, APPS_DIR)

EMAIL_HOST='mail.quantumimagery.com'
EMAIL_PORT=25
EMAIL_HOST_USER='robot@quantumimagery.com'
EMAIL_HOST_PASSWORD='E3Kfgozz7iMyb38N7ohb'
DEFAULT_FROM_EMAIL = 'GoodCloud'
SERVER_EMAIL = 'robot@agoodcloud.com'

ADMINS = (
     ('Steven Skoczen', 'steven@quantumimagery.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',               # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'skoczen_mycelium',      # Or path to database file if using sqlite3.
        'USER': 'skoczen_mycelium',      # Not used with sqlite3.
        'PASSWORD': '5bc651ec',          # Not used with sqlite3.
        'HOST': 'web58.webfaction.com',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}



# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True



MEDIA_ROOT = join(abspath(PROJECT_ROOT),"../media")
MEDIA_URL = 'http://www.agoodcloud.com/media/'
STATIC_URL = MEDIA_URL
ADMIN_MEDIA_PREFIX = "%sadmin/" % (MEDIA_URL)


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'd^bkm43rw#gmxbs4bvf)8)2)n=l9obc9-*022=hcm_s0w2bikt'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    'django.core.context_processors.auth',
    
    "qi_toolkit.context_processors.add_env_to_request",
)

ROOT_URLCONF = 'mycelium.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    
    'qi_toolkit',
    'django_nose',
    'google_analytics',

    'hi',
    'email_list',
    'rewrite',
)


TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    "%stemplates" % (PROJECT_ROOT),
)
GOOGLE_ANALYTICS_MODEL = True

SEND_BROKEN_LINK_EMAILS = True

    