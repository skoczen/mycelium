import datetime
from celery.task import task
from activities.models import Action, Activity
from johnny.utils import johnny_task_wrapper

@task
@johnny_task_wrapper
def save_action(account, staff, action_type, **kwargs):
                                 # person=None, organization=None, donation=None, shift=None, conversation=None

    now = datetime.datetime.now()
    just_now = now - datetime.timedelta(minutes=5)

    activity = Activity.objects.using("default").get_or_create(name=action_type)[0]
    if Action.objects.using("default").filter(account=account, staff=staff, activity=activity, date__gte=just_now, **kwargs).count() == 0:
        Action.objects.using("default").create(account=account, staff=staff, activity=activity, date=now, **kwargs)
