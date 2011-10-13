from celery.task import task
from johnny import cache as jcache

@task
def create_tag_group(tag):
    try:
        tag.create_tag_group_if_needed()
        jcache.invalidate("groups.GroupSearchProxy")
        jcache.invalidate("groups.TagGroup")
    except:
        from django.core.mail import mail_admins
        from qi_toolkit.helpers import exception_string
        mail_admins("Exception creating tag group", exception_string(), fail_silently=True)