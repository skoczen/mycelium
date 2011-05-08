from celery.decorators import task
from django.core.cache import cache

@task
def regnerate_all_rulegroup_search_results_for_account(cls, account):
    for g in cls.objects_by_account(account).all():
        cached_num = cache.get(g.cached_count_key)
        if g.members.count() != cached_num:
            g.regenerate_and_cache_search_results()
