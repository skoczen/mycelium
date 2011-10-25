from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
import subprocess
from os.path import abspath, join



class Command(BaseCommand):
    help = "Repopulate the search caches."
    __test__ = False

    def handle(self, *args, **options):
        from people.models import PeopleSearchProxy
        from organizations.models import OrganizationsSearchProxy
        from groups.models import GroupSearchProxy
        from spreadsheets.models import SpreadsheetSearchProxy

        print "Repopulating people...",
        PeopleSearchProxy.populate_cache()
        print "done."
        print "Repopulating organizations..."
        OrganizationsSearchProxy.populate_cache()
        print "done."
        print "Repopulating groups..."
        GroupSearchProxy.populate_cache()
        print "done."
        print "Repopulating spreadsheets..."
        SpreadsheetSearchProxy.populate_cache()
        print "done."
        