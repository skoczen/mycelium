from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from taggit.managers import TaggableManager
from accounts.models import AccountBasedModel

from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^generic_tags\.manager.TaggableManager"])



import re
DIGIT_REGEX = re.compile(r'[^\d]+')
NO_NAME_STRING_PERSON = _("Unnamed Person")
NO_NAME_STRING_ORGANIZATION = _("Unnamed Organization")
from generic_tags.models import TagSet, Tag
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.core.cache import cache
from mycelium_core.models import SearchableItemProxy
from mycelium_core.tasks import update_proxy_results_db_cache, put_in_cache_forever
from data_import.models import PotentiallyImportedModel

class OrganizationType(AccountBasedModel, models.Model):
    internal_name = models.CharField(max_length=255)
    friendly_name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.friendly_name

    class Meta(object):
        ordering = ("id",)

class AddressBase(models.Model):
    line_1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address Line 1")
    line_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address Line 2")
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "%(line_1)s, %(line_2)s, %(city)s, %(state)s %(postal_code)s" % (self.__dict__)

    class Meta(object):
        abstract = True
        verbose_name_plural = "Addresses"

class EmailAddressBase(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.email

    class Meta(object):
        abstract = True
        verbose_name_plural = "Email Addresses"

class PhoneNumberBase(models.Model):
    phone_number = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.phone_number

    class Meta(object):
        abstract = True


class Person(AccountBasedModel, SimpleSearchableModel, TimestampModelMixin, AddressBase, PhoneNumberBase, EmailAddressBase, PotentiallyImportedModel):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    
    search_fields = ["searchable_full_name","searchable_primary_email", "searchable_primary_phone_number"]
    contact_type = "person"
    
    class Meta(object):
        verbose_name_plural = "People"
        ordering = ("first_name", "last_name")

    def __unicode__(self):
        return u"%s" % (self.full_name)


    @models.permalink
    def get_absolute_url(self):
        return ('people:person', [str(self.id)])

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return "%s %s" % (self.first_name or "", self.last_name or "")
        else:
            return NO_NAME_STRING_PERSON
    
    @property
    def searchable_full_name(self):
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

    @property
    def searchable_primary_email(self):
        if self.primary_email:
            return self.primary_email
        else:
            return ''

    @property
    def primary_phone_number(self):
        if self.phone_number:
            return self.phone_number
        else:
            for e in self.jobs.all():
                if e.phone_number:
                    return e.phone_number
        return None

    @property
    def primary_email(self):
        if self.email:
            return self.email
        else:
            for e in self.jobs.all():
                if e.email:
                    return e.email
        return None

    @property
    def tagsets(self):
        return TagSet.objects_by_account(self.account).all()

    @property
    def search_result_row(self):
        # Ugh.
        return self.peopleandorganizationssearchproxy_set.all()[0].search_result_row


class Organization(AccountBasedModel, SimpleSearchableModel, AddressBase, TimestampModelMixin, PotentiallyImportedModel):
    name = models.CharField(max_length=255, blank=True, null=True)

    search_fields = ["full_name","searchable_primary_phone_number"]
    contact_type = "organization"
    organization_type = models.ForeignKey(OrganizationType, blank=True, null=True)
    organization_type_other_name = models.CharField(max_length=255, blank=True, null=True)
    primary_phone_number = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    twitter_username = models.CharField(max_length=255, blank=True, null=True)

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
        return ('people:organization', [str(self.id)])

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



class PeopleAndOrganizationsSearchProxy(SearchableItemProxy):
    SEARCH_GROUP_NAME = "people_and_orgs"
    person = models.ForeignKey(Person, blank=True, null=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)

    @property
    def obj(self):
        return self.person or self.organization or None

    @property
    def type(self):
        if self.person_id != None:
            return "person"
        elif self.organization_id != None:
            return "organization"
        return None
    
    @property
    def obj_id(self):
        if self.person_id:
            return self.person_id
        elif self.organization_id:
            return self.organization_id
        else:
            return None

    def get_sorting_name(self):
        sn = ""
        if self.person_id:
            sn =  self.person.full_name
        elif self.organization_id:
            sn = self.organization.searchable_name
        if sn == NO_NAME_STRING_PERSON or sn == NO_NAME_STRING_ORGANIZATION:
            sn = ""
        return sn
        
    @property
    def search_result_row(self):
        if cache.get(self.cache_name):
            return cache.get(self.cache_name)
        elif self.cached_search_result:
            put_in_cache_forever(self.cache_name,self.cached_search_result)
            return self.cached_search_result
        else:
            ss = self.render_result_row()
            # popping over to celery
            put_in_cache_forever(self.cache_name,ss)
            update_proxy_results_db_cache.delay(self,ss)
            return ss

    @property
    def cache_name(self):
        return "%s-%s-%s" % (self.search_group_name, self.type, self.obj_id)

    def generate_search_string(self):
        return self.obj.qi_simple_searchable_search_field

    def render_result_row(self):
        if self.person_id:
            return render_to_string("people/_search_result_row_person.html",{'obj':self.obj})
        elif self.organization_id:
            return render_to_string("people/_search_result_row_organization.html",{'obj':self.obj})
        else:
            return ""
        
    @classmethod
    def people_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        proxy, nil = cls.raw_objects.get_or_create(account=instance.account, person=instance, search_group_name=cls.SEARCH_GROUP_NAME)
        cache.delete(proxy.cache_name)
        proxy.save()


    @classmethod
    def organization_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        proxy, nil = cls.raw_objects.get_or_create(account=instance.account, organization=instance, search_group_name=cls.SEARCH_GROUP_NAME)
        cache.delete(proxy.cache_name)
        proxy.save()

    @classmethod
    def related_people_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        cls.people_record_changed(sender, instance.person, *args, **kwargs)

    @classmethod
    def related_organization_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        cls.organization_record_changed(sender, instance.organization, *args, **kwargs)


    @classmethod
    def populate_cache(cls):
        [cls.people_record_changed(Person,p) for p in Person.raw_objects.all()]
        [cls.organization_record_changed(Organization,o) for o in Organization.raw_objects.all()]

    @classmethod
    def resave_all_people_and_organizations(cls):
        [p.save() for p in Person.raw_objects.all()]
        [o.save() for o in Organization.raw_objects.all()]


    class Meta(SearchableItemProxy.Meta):
        verbose_name_plural = "PeopleAndOrganizationsSearchProxies"

        
post_save.connect(PeopleAndOrganizationsSearchProxy.people_record_changed,sender=Person)
post_save.connect(PeopleAndOrganizationsSearchProxy.organization_record_changed,sender=Organization)
post_save.connect(PeopleAndOrganizationsSearchProxy.related_organization_record_changed,sender=Employee)
post_save.connect(PeopleAndOrganizationsSearchProxy.related_people_record_changed,sender=Employee)
