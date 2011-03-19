from celery.schedules import crontab
from celery.decorators import periodic_task
from django.conf import settings
# from django.core.management import call_command
import os

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

# @periodic_task(run_every=crontab(hour="*", minute="*", day_of_week="*"))
@periodic_task(run_every=crontab(hour="2", minute="1", day_of_week="*"))
def offsite_backups():
    opts = {
        'backup_file': "/tmp/current_backup_%s.dump" % settings.ENV,
        'offsite_server_dir': settings.OFFSITE_BACKUP_DIR,
        'env': settings.ENV,
    }
    os.system("./manage.py dumpdb > %(backup_file)s;bzip2 -9q %(backup_file)s;scp %(backup_file)s.bz2 %(offsite_server_dir)sdaily_%(env)s_`date +%%F`.dump.bz2; rm %(backup_file)s.bz2" % opts)
