from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Plan(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)


class Account(models.Model):
    name = models.CharField(max_length=255)
    subdomain = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    plan = models.ForeignKey(Plan)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)


class AccessLevel(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)


class UserAccount(models.Model):
    user = models.ForeignKey(User)
    account = models.ForeignKey(Account)
    access_level = models.ForeignKey(AccessLevel)
    
    def __unicode__(self):
        return "%s with %s" % (self.user, self.account)

    class Meta(object):
        ordering = ("name",)
