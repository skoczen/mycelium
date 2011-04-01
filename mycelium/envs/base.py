# Django settings for mycelium project.
DEBUG = False
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_DEBUG = DEBUG

import os, sys
from os.path import abspath, dirname, join
gettext = lambda s: s

PROJECT_ROOT = join(abspath(dirname(__file__)), "../")
STATIC_ROOT = join(abspath(PROJECT_ROOT),"../media")
MEDIA_ROOT = abspath(STATIC_ROOT)
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
SEND_BROKEN_LINK_EMAILS = True

ADMINS = (
     ('Steven Skoczen', 'steven@quantumimagery.com'),
)
MANAGERS = ADMINS
MANAGERS += (
    ('Tom Noble', 'tomnoble6@gmail.com'),
)


TIME_ZONE = None
LANGUAGE_CODE = 'en'
LANGUAGES = (
        # ('fr', gettext('French')),
        # ('de', gettext('German')),
        ('en', gettext('English')),
)
SITE_ID = 1
USE_I18N = True
# USE_L10N = True



# Make this unique, and don't share it with anybody.
SECRET_KEY = 'd^bkm43rw#gmxbs4bvf)8)2)n=l9obc9-*022=hcm_s0w2bikt'

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
    'pagination.middleware.PaginationMiddleware',
    
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    # 'cms.middleware.multilingual.MultilingualURLMiddleware',
    'cms.middleware.media.PlaceholderMediaMiddleware',
)

SSL_ENABLED = True

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    'django.core.context_processors.auth',
    
    "cms.context_processors.media",
    "qi_toolkit.context_processors.add_env_to_request",
    "qi_toolkit.context_processors.add_favicon_to_request",    
    "mycelium_core.context_processors.cdn_media_url",
)

DATE_INPUT_FORMATS = ('%m/%d/%Y', '%Y-%m-%d', '%m/%d/%y', '%b %d %Y',
'%b %d, %Y', '%d %b %Y', '%d %b, %Y', '%B %d %Y',
'%B %d, %Y', '%d %B %Y', '%d %B, %Y')

ROOT_URLCONF = 'mycelium.urls'


INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',

    'qi_toolkit',
    'google_analytics',
    'django_extensions',
    'pagination',
    'south',
    'gunicorn',
    'sorl.thumbnail',
    'django_nose',
    'djcelery',
    'taggit',
    'taggit_templatetags',
    'django_jenkins',
    'django_dumpdb',
    'django_ses',
    'mediasync',

    'cms',
    'mptt',
    'menus',
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.link',
    'cms.plugins.file',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'form_designer',
    'tinymce',

    'marketing_site',
    'email_list',
    'rewrite',
    'people',
    'mycelium_core',
    'reports',
    'import',
    'logo_maker',
    'volunteers',
    'conversations',
    'donors',
    'recent_activity',
    'generic_tags',
    'groups',


    'djangosanetesting',
)

TEMPLATE_DIRS = (
    "%stemplates" % (PROJECT_ROOT),
)
GOOGLE_ANALYTICS_MODEL = True


CMS_TEMPLATES = (
    ('marketing_site/home.html', 'Home Page'),
    ('marketing_site/normal_page.html', 'Normal Page'),
    ('marketing_site/about_us.html', 'About Us'),    
)
CMS_MENU_TITLE_OVERWRITE = True
CMS_SEO_FIELDS = True
CMS_APPLICATIONS_URLS = (
    ('marketing_site.urls', 'Marketing Site'),
)
CMS_USE_TINYMCE = True
GOOGLE_MAPS_KEY = "ABQIAAAAHhU2Kv9Iz8Fh-GRXaplHqxRHA9ICmOpg9-1g76S5BMdlTE0SKRRfIwbO5xyH_2XiYLy9Wt8qQ9Ymz"

SESSION_COOKIE_AGE = 1209600
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

ENV = None

# qi toolkit
DEFAULT_SMOKE_TEST_OPTIONS = {
    'verbose'           : False,
}
OFFSITE_BACKUP_DIR = "aglzen@quantumimagery.com:/home/aglzen/mycelium/data/"


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = ['--where=apps', '-s']

FORCE_SELENIUM_TESTS = False
SELENIUM_BROWSER_COMMAND = "*safari"
LIVE_SERVER_PORT = 8099
SELENIUM_PORT = 64444

SOUTH_LOGGING_ON = True
SOUTH_LOGGING_FILE = "/dev/null"

THUMBNAIL_FORMAT = "PNG"
THUMBNAIL_COLORSPACE = None

# celery / rabbitmq
BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "mycelium"
BROKER_PASSWORD = "68WXmV6K49r8veczVaUK"
BROKER_VHOST = "digitalmycelium"
CELERY_RESULT_BACKEND = "amqp"
import djcelery
djcelery.setup_loader()

# for initial sync
CELERY_RESULT_BACKEND = "database"

# sorl
THUMBNAIL_PREFIX = "_cache/"


# DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = 'AKIAJTNZWCZDOIDWFR4A'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = "goodcloud1"
AWS_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME

CDN_MEDIA_URL = "https://%s.s3.amazonaws.com/" % AWS_STORAGE_BUCKET_NAME

# get git commit
from git import Repo
GIT_CURRENT_SHA = Repo(PROJECT_ROOT).head.reference.commit.hexsha



# django-mediasync
MEDIASYNC = {
    'BACKEND': 'mediasync.backends.s3',
    'AWS_KEY': AWS_ACCESS_KEY_ID,
    'AWS_SECRET': AWS_SECRET_ACCESS_KEY,
    'AWS_BUCKET': AWS_STORAGE_BUCKET_NAME,
    'CACHE_BUSTER': GIT_CURRENT_SHA,
    # 'PROCESSORS': (
    #     'mediasync.processors.slim.css_minifier',
    #     'mediasync.processors.slim.js_minifier',
    # ),
    'PROCESSORS': (
        'mediasync.processors.yuicompressor.css_minifier',
        'mediasync.processors.yuicompressor.js_minifier',
    ),    
    'YUI_COMPRESSOR_PATH': join(abspath(LIB_DIR), 'yuicompressor.jar'),
    'JOINED': {
        'js/mycelium/mycelium_base_all.js': [   "/js/contrib/jquery.scrollTo-min.js", 
                                                "/js/contrib/jquery.toggleval.js", 
                                                "/js/contrib/jquery.hotkeys-0.7.9.min.js",
                                                "/js/contrib/jquery.ajax.queue.js", 
                                                "/js/contrib/jquery.autogrow.js", 
                                                "/js/contrib/jquery.form.js", 
                                                "/js/contrib/jquery.ba-bbq.min.js", 
                                                "/js/contrib/autocolumn.min.js",
                                                "/js/mycelium/mycelium_elements.js",
                                                "/js/mycelium/mycelium_search.js",
                                            ]
    }



}
MEDIASYNC['SERVE_REMOTE'] = True
