from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from people.models import Person
from django.db.models.signals import post_save
import datetime
from taggit.managers import TaggableManager


class Group(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

class SmartGroup(TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True)

class SmartGroupRule(models.Model):
    group = models.ForeignKey(SmartGroup)
