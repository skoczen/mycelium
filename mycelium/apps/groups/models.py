from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from django.db.models.signals import post_save
import datetime
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^generic_tags\.manager.TaggableManager"])

class Group(TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __unicode__(self):
        return "%s" % self.name

    @property
    def members(self):
        from people.models import Person
        return Person.objects.filter(pk__in=self.groupmembership_set.all())

    class Meta(object):
        ordering = ("name",)

class GroupMembership(TimestampModelMixin):
    group = models.ForeignKey(Group, blank=True, null=True)
    person = models.ForeignKey('people.Person', blank=True, null=True)

    def __unicode__(self):
        return "%s in %s" % self.group, self.person

    class Meta(object):
        ordering = ("group","person",)

class SmartGroup(TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)

class SmartGroupRule(models.Model):
    group = models.ForeignKey(SmartGroup)

    def __unicode__(self):
        return "Rule for %s" % self.group

    class Meta(object):
        ordering = ("group","id",)