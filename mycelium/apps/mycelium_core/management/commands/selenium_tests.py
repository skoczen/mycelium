from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
import subprocess
from os.path import abspath, join


class Command(BaseCommand):
    help = "Run the selenium tests."
    __test__ = False

    def handle(self, *args, **options):
        output = file('/dev/null', 'a+')
        sel_command =  "java -jar %(lib_path)s/selenium-server.jar -timeout 30 -port %(selenium_port)s -userExtensions %(lib_path)s/user-extensions.js" % {'lib_path' :join(abspath(settings.PROJECT_ROOT), "lib"), "selenium_port":settings.SELENIUM_PORT}
        gun_command =  "~/.virtualenvs/mycelium/bin/python manage.py run_gunicorn -w 2 -b 0.0.0.0:%s --settings=envs.tests_selenium" % settings.LIVE_SERVER_PORT
        # cel_command =  "python manage.py celeryd"
        selenium_subprocess = subprocess.Popen(sel_command,shell=True, stderr=output, stdout=output)
        gunicorn_subprocess = subprocess.Popen(gun_command,shell=True, stderr=output, stdout=output)
        # celery_subprocess = subprocess.Popen(cel_command,shell=True, stderr=output, stdout=output)
        try:
            call_command('test', "--with-selenium", "--with-selenium-fixtures", *args, **options )
            output.close()    
        except:
            pass
        
        try:
            selenium_subprocess.kill()
        except:
            pass

        try:
            gunicorn_subprocess.kill()
        except:
            pass

        # celery_subprocess.kill()
