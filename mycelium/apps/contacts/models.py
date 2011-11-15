from django.db import models
from contacts import CONTACT_TYPE_CHOICES

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


class ContactMethod(models.Model):
    METHOD_CHOICES = CONTACT_TYPE_CHOICES
    contact_type = models.CharField(max_length=20, choices=METHOD_CHOICES, default=METHOD_CHOICES[0][0])
    primary = models.BooleanField(default=False)

    class Meta(object):
        abstract = True