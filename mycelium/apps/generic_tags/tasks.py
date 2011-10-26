from celery.task import task
from johnny.utils import johnny_task_wrapper

@task
@johnny_task_wrapper
def create_tag_group(tag):
    from generic_tags.models import Tag
    try:
        t = Tag.objects.using("default").get(pk=tag.pk)
        t.create_tag_group_if_needed()
    except:
        from django.core.mail import mail_admins
        from qi_toolkit.helpers import exception_string
        mail_admins("Exception creating tag group", exception_string(), fail_silently=True)