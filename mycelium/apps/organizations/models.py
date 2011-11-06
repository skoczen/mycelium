from django.db import models
from django.utils.translation import ugettext as _
from django.db import transaction

from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from taggit.managers import TaggableManager
from accounts.models import AccountBasedModel
from people.models import AddressBase, Person, PeopleSearchProxy

from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^generic_tags\.manager.TaggableManager"])

import re

DIGIT_REGEX = re.compile(r'[^\d]+')
NO_NAME_STRING_ORGANIZATION = _("Unnamed Organization")

from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.core.cache import cache
from mycelium_core.models import SearchableItemProxy
from mycelium_core.tasks import update_proxy_results_db_cache, put_in_cache_forever, update_proxy
from data_import.models import PotentiallyImportedModel


class OrganizationType(AccountBasedModel, models.Model):
    internal_name = models.CharField(max_length=255)
    friendly_name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.friendly_name

    class Meta(object):
        ordering = ("id",)


class Organization(AccountBasedModel, SimpleSearchableModel, AddressBase, TimestampModelMixin, PotentiallyImportedModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    search_fields = ["full_name","searchable_primary_phone_number"]
    contact_type = "organization"
    organization_type = models.ForeignKey(OrganizationType, blank=True, null=True)
    organization_type_other_name = models.CharField(max_length=255, blank=True, null=True)
    primary_phone_number = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    twitter_username = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ("name",)

    tags = TaggableManager()
    def alphabetical_tags(self):
        return self.tags.all().order_by("name")
    
    @property
    def full_name(self):
        if self.name:
            return self.name
        else:
            return NO_NAME_STRING_ORGANIZATION

    @property
    def searchable_name(self):
        if self.full_name:
            return self.full_name
        else:
            return ""


    @property
    def searchable_primary_phone_number(self):
        if self.primary_phone_number:
            return DIGIT_REGEX.sub('', "%s" % self.primary_phone_number)
        else:
            return ''
            
    def __unicode__(self):
        return "%s" % (self.name,)

    @models.permalink
    def get_absolute_url(self):
        return ('organizations:organization', [str(self.id)])

class Employee(AccountBasedModel, TimestampModelMixin):
    person = models.ForeignKey(Person, related_name="jobs")
    role = models.CharField(max_length=255, blank=True, null=True, verbose_name="Title")
    email = models.CharField(max_length=255, blank=True, null=True,verbose_name="Email")
    phone_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Phone number")
    organization = models.ForeignKey(Organization, related_name="employees")
    
    def __unicode__(self):
        return "%s - %s at %s" % (self.person, self.role, self.organization)
    
    class Meta:
        ordering = ("organization","person",)



class OrganizationsSearchProxy(SearchableItemProxy):
    SEARCH_GROUP_NAME = "organizations"
    organization = models.ForeignKey(Organization, blank=True, null=True)

    @property
    def obj(self):
        return self.organization or None

    @property
    def type(self):
        if self.organization_id != None:
            return "organization"
        return None
    
    @property
    def obj_id(self):
        if self.organization_id:
            return self.organization_id
        else:
            return None

    def get_sorting_name(self):
        sn = ""
        if self.organization_id:
            sn = self.organization.searchable_name
        if sn == NO_NAME_STRING_ORGANIZATION:
            sn = ""
        return sn
        
    @property
    def search_result_row(self):
        if cache.get(self.cache_name):
            return cache.get(self.cache_name)
        elif self.cached_search_result:
            try:
                transaction.commit()
            except:
                pass
            put_in_cache_forever.delay(self.cache_name,self.cached_search_result)
            return self.cached_search_result
        else:
            ss = self.render_result_row()
            # popping over to celery
            try:
                transaction.commit()
            except:
                pass
            put_in_cache_forever.delay(self.cache_name,ss)
            update_proxy_results_db_cache.delay(self,ss)
            return ss

    @property
    def cache_name(self):
        return "%s-%s-%s" % (self.search_group_name, self.type, self.obj_id)

    def generate_search_string(self):
        return self.obj.qi_simple_searchable_search_field

    def render_result_row(self):
        if self.organization_id:
            return render_to_string("organizations/_search_result_row_organization.html",{'obj':self.obj})
        else:
            return ""

    @classmethod
    def organization_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        proxy, nil = cls.raw_objects.get_or_create(account=instance.account, organization=instance, search_group_name=cls.SEARCH_GROUP_NAME)
        cache.delete(proxy.cache_name)
        update_proxy.delay(cls, proxy)

    @classmethod
    def related_organization_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        cls.organization_record_changed(sender, instance.organization, *args, **kwargs)

    @classmethod
    def populate_cache(cls):
        [cls.organization_record_changed(Organization,o) for o in Organization.raw_objects.all()]

    @classmethod
    def resave_all_organizations(cls, verbose=False):
        counter = 0
        if verbose:
            total_count = Organization.raw_objects.all().count()
        for o in Organization.raw_objects.all():
            o.save()
            if verbose:
                counter += 1
                if counter % 100 == 0:
                    print "%s/%s" % (counter, total_count)

    class Meta(SearchableItemProxy.Meta):
        verbose_name_plural = "OrganizationsSearchProxies"

        
post_save.connect(OrganizationsSearchProxy.organization_record_changed,sender=Organization)
post_save.connect(OrganizationsSearchProxy.related_organization_record_changed,sender=Employee)
post_save.connect(PeopleSearchProxy.related_people_record_changed,sender=Employee)
