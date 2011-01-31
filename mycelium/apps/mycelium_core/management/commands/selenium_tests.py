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
        sel_command =  "java -jar %(lib_path)s/selenium-server.jar  -timeout 30 -port 4444 -userExtensions %(lib_path)s/user-extensions.js" % {'lib_path' :join(abspath(settings.PROJECT_ROOT), "lib")}
        selenium_subprocess = subprocess.Popen(sel_command,shell=True, stderr=output, stdout=output)
        try:
            call_command('test', "--with-django", "--with-selenium", "--with-djangoliveserver", *args, path=settings.PROJECT_ROOT, **options )
        except:
            pass
        output.close()
        selenium_subprocess.kill()
