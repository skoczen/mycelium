from celery.schedules import crontab
from celery.decorators import periodic_task
from django.core.mail import send_mail
from django.conf import settings

# this will run every minute, see http://celeryproject.org/docs/reference/celery.task.schedules.html#celery.task.schedules.crontab
@periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
def test():    
    print "firing test task"
    if settings.ENV == "DEV":
        fh = open("/Users/skoczen/Desktop/celery_test","a")
    else:    
        fh = open("/var/www/celery_test","a")
    fh.write("Oh hi\n")
    fh.close()