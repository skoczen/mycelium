from celery.schedules import crontab
from celery.decorators import periodic_task, task
from django.conf import settings
from django.core.cache import cache
from johnny import cache as johnny_cache
from johnny.utils import johnny_task_wrapper

@task
@johnny_task_wrapper
def test():    
    print "firing test task"
    if settings.ENV == "DEV":
        fh = open("/Users/skoczen/Desktop/celery_test","a")
    else:    
        fh = open("/var/www/celery_test","a")
    fh.write("Oh hi\n")
    fh.close()

@task
@johnny_task_wrapper
def update_proxy_results_db_cache(cls, proxy_obj, new_result_string):
    px = cls.objects.using("default").get(pk=proxy_obj.pk)
    px.cached_search_result = new_result_string
    px.save()
    johnny_cache.invalidate(px)


@task
def put_in_cache_forever(key, val):
    cache.set(key, val, 0)