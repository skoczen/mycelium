from celery.task import task
from django.core.cache import cache

@task
def update_proxy_results_db_cache(proxy_obj, new_result_string):
    from people.models import PeopleAndOrganizationsSearchProxy
    px = PeopleAndOrganizationsSearchProxy.objects.get(pk=proxy_obj.pk)
    px.cached_search_result = new_result_string
    px.save()

@task
def put_in_cache_forever(key, val):
    cache.set(key, val, 0)