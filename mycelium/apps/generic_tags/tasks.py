from celery.task import task
from johnny import cache as jcache

@task
def create_tag_group(tag):
    tag.create_tag_group_if_needed()
    jcache.invalidate("groups.GroupSearchProxy")
    jcache.invalidate("groups.TagGroup")