from celery.task import task

@task
def create_tag_group(tag_id):
    from generic_tags.models import Tag
    try:
        t = Tag.objects.using("default").get(pk=tag_id)
        t.create_tag_group_if_needed()
    except:
        from django.core.mail import mail_admins
        from qi_toolkit.helpers import exception_string
        mail_admins("Exception creating tag group", exception_string(), fail_silently=True)