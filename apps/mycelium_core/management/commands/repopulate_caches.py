from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management import call_command
import subprocess
from os.path import abspath, join

from people.models import PeopleSearchProxy
from organizations.models import OrganizationsSearchProxy
from groups.models import GroupSearchProxy

class Command(BaseCommand):
    help = "Repopulate the search caches."
    __test__ = False

    def handle(self, *args, **options):
        PeopleSearchProxy.populate_cache()
        OrganizationsSearchProxy.populate_cache()
        GroupSearchProxy.populate_cache()