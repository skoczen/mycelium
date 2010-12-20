from django.db import models
from django.utils.translation import ugettext as _

class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    
    class Meta(object):
        verbose_name_plural = "People"

class ContactMethodType(models.Model):
    internal_name = models.CharField(max_length=255)
    friendly_name = models.CharField(max_length=255)

class ContactMethod(models.Model):
    person = models.ForeignKey(Person)
    contact_type = models.ForeignKey(ContactMethodType)
    primary = models.BooleanField(default=False)

    class Meta(object):
        abstract = True

class EmailAddress(ContactMethod):
    email = models.EmailField(max_length=255)

    class Meta(object):
        verbose_name_plural = "Email Addresses"

class PhoneNumber(ContactMethod):
    phone = models.CharField(max_length=255)


class Address(ContactMethod):
    line_1 = models.CharField(max_length=255)
    line_2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)

    class Meta(object):
        verbose_name_plural = "Addresses"
