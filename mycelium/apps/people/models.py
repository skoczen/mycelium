from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin

import re
DIGIT_REGEX = re.compile(r'[^\d]+')

class OrganizationType(models.Model):
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


class Person(SimpleSearchableModel, TimestampModelMixin, AddressBase, PhoneNumberBase, EmailAddressBase):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    
    search_fields = ["first_name","last_name","primary_email", "searchable_primary_phone_number"]
    contact_type = "person"
    
    class Meta(object):
        verbose_name_plural = "People"
        ordering = ("first_name", "last_name")

    def __unicode__(self):
        return u"%s" % (self.full_name)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
    
    @property
    def searchable_primary_phone_number(self):
        if self.phone_number:
            return DIGIT_REGEX.sub('', "%s" % self.phone_number)
        else:
            return ''
        
    @property
    def primary_phone_number(self):
        return self.phone_number

    @property
    def primary_email(self):
        return self.email


class Organization(SimpleSearchableModel, AddressBase, TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True)

    search_fields = ["name","searchable_primary_phone_number"]
    contact_type = "organization"
    organization_type = models.ForeignKey(OrganizationType, blank=True, null=True)
    organization_type_other_name = models.CharField(max_length=255, blank=True, null=True)
    primary_phone_number = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    twitter_username = models.CharField(max_length=255, blank=True, null=True)

    @property
    def searchable_primary_phone_number(self):
        if self.primary_phone_number:
            return DIGIT_REGEX.sub('', "%s" % self.primary_phone_number)
        else:
            return ''
            
    def __unicode__(self):
        return "%s" % (self.name,)

class Employee(TimestampModelMixin):
    person = models.ForeignKey(Person, related_name="jobs")
    role = models.CharField(max_length=255, blank=True, null=True, verbose_name="Role")
    email = models.CharField(max_length=255, blank=True, null=True,verbose_name="Role email")
    phone_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Role phone number")
    organization = models.ForeignKey(Organization, related_name="employees")
    
    def __unicode__(self):
        return "%s - %s at %s" % (self.person, self.role, self.organization)
    
    class Meta:
        ordering = ("organization","person",)


from django.core.cache import cache
from django.db.models.signals import post_save
#TODO: Abstract this into the qi_toolkit or something better
class SearchableItemProxy(SimpleSearchableModel):
    # models = []
    search_group_name = models.CharField(max_length=255)
    search_string = models.TextField(blank=True, null=True)
    cached_search_result = models.TextField(blank=True, null=True)

    @property
    def cache_name(self):
        # Define this on subclassing.
        return "%s-%s" % (self.search_group_name, self.pk)
    
    def generate_search_string(self):
        # Define this on subclassing.
        return "%s" % (self.pk)

    def __unicode__(self):
        return self.generate_search_string()

    class Meta(object):
        abstract = True

    def save(self,*args,**kwargs):
        self.search_string = self.generate_search_string()
        ss = self.render_result_row()
        self.cached_search_result = ss
        cache.set(self.cache_name, ss, 9000000)
        super(SearchableItemProxy,self).save(*args,**kwargs)

from django.template.loader import render_to_string
from people.tasks import *
class PeopleAndOrganizationsSearchProxy(SearchableItemProxy):
    SEARCH_GROUP_NAME = "people_and_orgs"
    person = models.ForeignKey(Person, blank=True, null=True)
    organization = models.ForeignKey(Organization, blank=True, null=True)

    @property
    def obj(self):
        return self.person or self.organization or None

    @property
    def type(self):
        if self.person:
            return "person"
        elif self.organization:
            return "organization"
        return None


    @property
    def search_result_row(self):
        if cache.get(self.cache_name):
            return cache.get(self.cache_name)
        elif self.cached_search_result:
            cache.set(self.cache_name,self.cached_search_result, 9000000)
            return self.cached_search_result
        else:
            ss = self.render_result_row()
            cache.set(self.cache_name,ss, 9000000)
            # popping over to celery
            update_proxy_results_db_cache.delay(self,ss)
            return ss

    @property
    def cache_name(self):
        return "%s-%s-%s" % (self.search_group_name, self.type, self.obj.pk)

    def generate_search_string(self):
        return self.obj.qi_simple_searchable_search_field
        # return "%s" % (self.pk)    

    def render_result_row(self):
        if self.person:
            return render_to_string("people/_search_result_row_person.html",{'obj':self.obj})
        elif self.organization:
            return render_to_string("people/_search_result_row_organization.html",{'obj':self.obj})
        else:
            return ""
        
    @classmethod
    def people_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        proxy, nil = cls.objects.get_or_create(person=instance, search_group_name=cls.SEARCH_GROUP_NAME)
        cache.delete(proxy.cache_name)
        proxy.save()

    @classmethod
    def organization_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        proxy, nil = cls.objects.get_or_create(organization=instance, search_group_name=cls.SEARCH_GROUP_NAME)
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
        [cls.people_record_changed(Person,p) for p in Person.objects.all()]
        [cls.organization_record_changed(Organization,o) for o in Organization.objects.all()]

    class Meta(object):
        verbose_name_plural = "PeopleAndOrganizationsSearchProxies"
        ordering = ("person", "organization")
        
post_save.connect(PeopleAndOrganizationsSearchProxy.people_record_changed,sender=Person)
post_save.connect(PeopleAndOrganizationsSearchProxy.organization_record_changed,sender=Organization)
post_save.connect(PeopleAndOrganizationsSearchProxy.related_organization_record_changed,sender=Employee)