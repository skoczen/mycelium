# exact copy of dev, plus settings.CELERY_ALWAYS_EAGER = True
from envs.dev import *
CELERY_ALWAYS_EAGER = True
BROKER_BACKEND = "memory"
