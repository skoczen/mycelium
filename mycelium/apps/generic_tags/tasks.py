from celery.task import task
from johnny.utils import johnny_task_wrapper

@task
@johnny_task_wrapper
def create_tag_group(tag_id):
    from generic_tags.models import Tag
    try:
        print tag_id
        print Tag.objects.all()
        t = Tag.objects.using("default").get(pk=tag_id)
        t.create_tag_group_if_needed()
    except:
        from django.core.mail import mail_admins
        from qi_toolkit.helpers import exception_string
        mail_admins("Exception creating tag group", exception_string(), fail_silently=True)