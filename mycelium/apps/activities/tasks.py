import datetime
from celery.task import task
from activities.models import Action, Activity


@task
def save_action(account, staff, action_type, **kwargs):
                                 # person=None, organization=None, donation=None, shift=None, conversation=None

    now = datetime.datetime.now()
    just_now = now - datetime.timedelta(minutes=5)

    print kwargs
    # This is failing on the conversation PK not failing its FK reference.  (and conversation only.)

    # get fresh.
    new_kwargs = {}
    for k,v in kwargs.iteritems():
        model = v.__class__
        try:
            new_kwargs[k] = model.objects.get(pk=v.pk)
        except:
            from qi_toolkit.helpers import print_exception
            print_exception()
            pass
    
    print new_kwargs

    activity = Activity.objects.get_or_create(name=action_type)[0]
    print Action.objects.filter(account=account, staff=staff, activity=activity, date__gte=just_now, **new_kwargs).count()
    if Action.objects.filter(account=account, staff=staff, activity=activity, date__gte=just_now, **new_kwargs).count() == 0:
        print Action.objects.create(account=account, staff=staff, activity=activity, date=now, **new_kwargs)

    