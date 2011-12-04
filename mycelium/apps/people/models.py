import re
import datetime

from django.db import models, transaction
from django.utils.translation import ugettext as _
from django.db.models import Sum
from django.template.loader import render_to_string
from django.db.models.signals import post_save
from django.core.cache import cache
from south.modelsinspector import add_ignored_fields

from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from accounts.models import AccountBasedModel
from contacts.models import AddressBase, EmailAddressBase, PhoneNumberBase, ContactMethod
from people import PHONE_CONTACT_TYPE_CHOICES
from generic_tags.models import TagSet
from mycelium_core.models import SearchableItemProxy
from mycelium_core.tasks import update_proxy_results_db_cache, put_in_cache_forever
from data_import.models import PotentiallyImportedModel

add_ignored_fields(["^generic_tags\.manager.TaggableManager"])
DIGIT_REGEX = re.compile(r'[^\d]+')
NO_NAME_STRING_PERSON = _("Unnamed Person")
NORMALIZED_BIRTH_YEAR = 2000  # should be a leap year for normalization's sake.
MONTHS = [
    (1,  _("January")),
    (2,  _("February")),
    (3,  _("March")),
    (4,  _("April")),
    (5,  _("May")),
    (6,  _("June")),
    (7,  _("July")),
    (8,  _("August")),
    (9,  _("September")),
    (10, _("October")),
    (11, _("November")),
    (12, _("December")),
]

ABBREV_MONTHS = [
    (1,  _("Jan.")),
    (2,  _("Feb.")),
    (3,  _("Mar.")),
    (4,  _("Apr.")),
    (5,  _("May")),
    (6,  _("June")),
    (7,  _("July")),
    (8,  _("Aug.")),
    (9,  _("Sep.")),
    (10, _("Oct.")),
    (11, _("Nov.")),
    (12, _("Dec.")),
]


class BirthdayBase(models.Model):
    birth_day           = models.IntegerField(blank=True, null=True, verbose_name="day")
    birth_month         = models.IntegerField(blank=True, null=True, choices=MONTHS, verbose_name="month")
    birth_year          = models.IntegerField(blank=True, null=True, verbose_name="year")
    actual_birthday     = models.DateField(blank=True, null=True)
    normalized_birthday = models.DateField(blank=True, null=True)
    age                 = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.best_birthday_description

    def save(self, *args, **kwargs):
        self.actual_birthday = None
        if self.birth_day and self.birth_month:
            self.normalized_birthday = datetime.date(year=NORMALIZED_BIRTH_YEAR, month=self.birth_month, day=self.birth_day)
            if self.birth_year:
                self.actual_birthday = datetime.date(year=self.birth_year, month=self.birth_month, day=self.birth_day)
                self.age = BirthdayBase.age_from_birthday(self.actual_birthday)
            else:
                self.age = None
                self.actual_birthday = None
        else:
            self.normalized_birthday = None

        super(BirthdayBase,self).save(*args, **kwargs)
    
    @property
    def best_birthday_text(self):
        if self.actual_birthday:
            return "%s %s, %s" % (self.get_birth_month_display(), self.birth_day, self.birth_year)
        elif self.normalized_birthday:
            return "%s %s" % (self.get_birth_month_display(), self.birth_day)
        else:
            return ""
    
    @property
    def abbreviated_birth_month(self):
        month = ""
        if self.birth_month:
            for k,v in ABBREV_MONTHS:
                if k == self.birth_month:
                    month = v
        return month

    @property
    def birthday_abbrev_month_day_text(self):
        if self.normalized_birthday:
            return "%s %s" % (self.abbreviated_birth_month, self.birth_day)
        else:
            return ""

    @property
    def next_or_todays_birthday_age(self):
        if self.actual_birthday:
            today = datetime.date.today()
            if self.actual_birthday.day == today.day and self.actual_birthday.month == today.month:
                return self.age
            else:
                return self.age + 1
        else:
            return None
    
    @classmethod
    def age_from_birthday(cls, birthdate):
        from math import floor
        return int(floor( (datetime.date.today() - birthdate).days /365.25))

    class Meta(object):
        abstract = True


class Person(AccountBasedModel, SimpleSearchableModel, TimestampModelMixin, AddressBase, BirthdayBase, PotentiallyImportedModel):
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
        if self.phone_numbers:
            return self.phone_numbers.order_by("primary",)[0]
        else:
            for e in self.jobs.all():
                if e.phone_number:
                    return e.phone_number
        return None

    @property
    def phone_numbers(self):
        return self.personphonenumber_set.all()

    @property
    def primary_email(self):
        if self.emails:
            return self.emails.order_by("primary",)[0]
        else:
            for e in self.jobs.all():
                if e.email:
                    return e.email
        return None

    @property
    def emails(self):
        return self.personemailaddress_set.all()

    @property
    def tagsets(self):
        return TagSet.objects_by_account(self.account).all()

    @property
    def search_result_row(self):
        # Ugh.
        return self.peoplesearchproxy_set.all()[0].search_result_row

    @property
    def employed(self):
        return self.jobs.count() > 0

    @property
    def primary_job(self):
        if self.employed:
            return self.jobs.all()[0]
        else:
            return None


    def volunteer_hours_for_year(self, year):
        this_year_start = datetime.date(year,1,1)
        next_year = datetime.date(year+1,1,1)
        return self.volunteer.completedshift_set.filter(date__gte=this_year_start).filter(date__lt=next_year).distinct().aggregate(Sum('duration'))["duration__sum"] or 0

    def donation_total_for_year(self, year):
        this_year_start = datetime.date(year,1,1)
        next_year = datetime.date(year+1,1,1)
        return self.donor.donation_set.filter(date__gte=this_year_start).filter(date__lt=next_year).distinct().aggregate(Sum('amount'))["amount__sum"] or 0

    @property
    def volunteer_hours_all_time(self):
        return self.volunteer.completedshift_set.distinct().aggregate(Sum('duration'))["duration__sum"] or 0

    @property
    def donation_totals_all_time(self):
        return self.donor.donation_set.distinct().aggregate(Sum('amount'))["amount__sum"] or 0
    
    @property
    def conversations(self):
        return self.conversation_set.all()


class PersonContactMethod(AccountBasedModel):
    person = models.ForeignKey(Person)
    
    class Meta(object):
        abstract = True



class EmailAddress(EmailAddressBase, ContactMethod):
    pass

class PhoneNumber(PhoneNumberBase, ContactMethod):
    METHOD_CHOICES = PHONE_CONTACT_TYPE_CHOICES
    pass

class PersonEmailAddress(EmailAddress, PersonContactMethod):
    class Meta:
        ordering = ("-primary",)

class PersonPhoneNumber(PhoneNumber, PersonContactMethod):
    class Meta:
        ordering = ("-primary",)

class PeopleSearchProxy(SearchableItemProxy):
    SEARCH_GROUP_NAME = "people"
    person = models.ForeignKey(Person, blank=True, null=True)

    @property
    def obj(self):
        return self.person or None

    @property
    def type(self):
        if self.person_id != None:
            return "person"
        return None
    
    @property
    def obj_id(self):
        if self.person_id:
            return self.person_id
        else:
            return None

    def get_sorting_name(self):
        sn = ""
        if self.person_id:
            sn =  self.person.full_name
        if sn == NO_NAME_STRING_PERSON:
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
        if self.person_id:
            return render_to_string("people/_search_result_row_person.html",{'obj':self.obj})
        else:
            return ""
        
    @classmethod
    def people_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        proxy, nil = cls.raw_objects.using("default").get_or_create(account=instance.account, person=instance, search_group_name=cls.SEARCH_GROUP_NAME)
        cache.delete(proxy.cache_name)
        proxy.save()

    @classmethod
    def related_people_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        cls.people_record_changed(sender, instance.person, *args, **kwargs)


    @classmethod
    def populate_cache(cls):
        [cls.people_record_changed(Person,p) for p in Person.raw_objects.all()]

    @classmethod
    def resave_all_people(cls, verbose=False):
        counter = 0
        if verbose:
            total_count = Person.raw_objects.all().count()
        for o in Person.raw_objects.all():
            o.save()
            if verbose:
                counter += 1
                if counter % 100 == 0:
                    print "%s/%s" % (counter, total_count)


    class Meta(SearchableItemProxy.Meta):
        verbose_name_plural = "PeopleSearchProxies"

        
post_save.connect(PeopleSearchProxy.people_record_changed,sender=Person)
post_save.connect(PeopleSearchProxy.related_people_record_changed,sender=PersonEmailAddress)
post_save.connect(PeopleSearchProxy.related_people_record_changed,sender=PersonPhoneNumber)
