from celery.decorators import task
from django.core.cache import cache
from accounts.models import Account
from johnny.utils import johnny_task_wrapper

@task
@johnny_task_wrapper
def regnerate_all_rulegroup_search_results_for_account(cls, account):
    # TODO:
    # set a cache key before calling this task.
    # task repeats while the key is set
    # first thing the task does is clear it.

    # End-behavior - recalculation only happens once per account, per change, and
    #                if a new recalculation is requested while a previous one is happening
    #                only one more loop will happen.
    account = Account.objects.using("default").get(pk=account.pk)
    for g in cls.objects_by_account(account).using("default").all():
        cached_num = cache.get(g.cached_count_key)
        if g.members.count() != cached_num:
            g.regenerate_and_cache_search_results()
