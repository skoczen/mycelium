from celery.schedules import crontab
from celery.decorators import periodic_task
from django.core.mail import send_mail
from django.conf import settings

# this will run every minute, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab
@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def test():    
    print "firing test task"
    fh = open("/var/log/celery_test","rw")
    fh.write("Oh hi\n")
    fh.close()