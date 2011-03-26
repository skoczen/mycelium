from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from django.db.models.signals import post_save
import datetime
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase


class Group(TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)

class GroupRule(models.Model):
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return "Rule for %s" % self.group

    class Meta(object):
        ordering = ("group","id",)
