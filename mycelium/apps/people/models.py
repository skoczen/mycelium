from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel

class Person(SimpleSearchableModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    
    class Meta(object):
        verbose_name_plural = "People"
        ordering = ("first_name", "last_name")

    def __unicode__(self):
        return u"%s" % (self.full_name())

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
    
    def primary_phone_number(self):
        phone_numbers = self.phonenumber_set.all()
        if phone_numbers.filter(primary=True).count() > 0:
            return phone_numbers.filter(primary=True)[0]
        else:
            if phone_numbers.count() > 0:
                return phone_numbers[0]
            else:
                return None

    def primary_email(self):
        emails = self.emailaddress_set.all()
        if emails.filter(primary=True).count() > 0:
            return emails.filter(primary=True)[0]
        else:
            if emails.count() > 0:
                return emails[0]
            else:
                return None

    def primary_address(self):
        addresses = self.address_set.all()
        if addresses.filter(primary=True).count() > 0:
            return addresses.filter(primary=True)[0]
        else:
            if addresses.count() > 0:
                return addresses[0]
            else:
                return None

class ContactMethodType(models.Model):
    internal_name = models.CharField(max_length=255)
    friendly_name = models.CharField(max_length=255)

class ContactMethod(models.Model):
    person = models.ForeignKey(Person)
    contact_type = models.ForeignKey(ContactMethodType, blank=True, null=True)
    primary = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(ContactMethod, self).save(*args, **kwargs)

    class Meta(object):
        abstract = True

class EmailAddress(ContactMethod):
    email = models.EmailField(max_length=255)

    def __unicode__(self):
        return "%s" % self.email

    class Meta(object):
        verbose_name_plural = "Email Addresses"

class PhoneNumber(ContactMethod):
    phone_number = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.phone_number

class Address(ContactMethod):
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)

    def __unicode__(self):
        return "%(line_1)s, %(line_2)s, %(city)s, %(state)s %(postal_code)s" % (self.__dict__)

    class Meta(object):
        verbose_name_plural = "Addresses"
