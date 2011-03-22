from celery.task import task
from django.core.cache import cache

@task
def update_proxy_results_db_cache(proxy_obj, new_result_string):
    proxy_obj.cached_search_result = new_result_string
    proxy_obj.save()

@task
def put_in_cache_forever(key, val):
    cache.set(key,val, 9000000)