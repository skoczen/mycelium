# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from johnny import cache as jcache
from django.core.cache import cache

from people.models import PeopleSearchProxy
from organizations.models import OrganizationsSearchProxy

class Migration(DataMigration):
    depends_on = (
        ("organizations", "0002_auto__del_organizationnew__del_organizationssearchproxynew__del_organi"),
    )

    def forwards(self, orm):
        "Write your forwards methods here."
        print "Starting update of search proxies. Clearing old proxies..."
        cache.clear()
        PeopleSearchProxy.objects.all().delete()
        print "Organizations cleared."
        OrganizationsSearchProxy.objects.all().delete()
        print "People cleared."

        print "Re-saving organizations..."
        OrganizationsSearchProxy.resave_all_organizations(verbose=True)
        print "Re-saving people..."
        PeopleSearchProxy.resave_all_people(verbose=True)
        print "Invalidating cache.."
        
        jcache.invalidate(PeopleSearchProxy)
        jcache.invalidate(OrganizationsSearchProxy)
        print "Done."

    def backwards(self, orm):
        "Write your backwards methods here."

