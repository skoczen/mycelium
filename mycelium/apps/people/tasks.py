from celery.task import task
import time

@task
def update_proxy_results_db_cache(proxy_obj, new_result_string):
    proxy_obj.cached_search_result = new_result_string
    proxy_obj.save()


