from celery.decorators import task

@task
def regnerate_all_rulegroup_search_results_for_account(cls, account):
    [g.regenerate_and_cache_search_results() for g in cls.objects_by_account(account).all()]
