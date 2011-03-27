from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from django.db.models.signals import post_save


from people.models import Person
from test_factory import Factory

class Group(TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)

    def members(self):
        if not hasattr(self,"cached_members"):
            self.cached_members = Person.objects.all().order_by("?")[:Factory.rand_int(10,100)]
        return self.cached_members

class GroupRule(models.Model):
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return "Rule for %s" % self.group

    class Meta(object):
        ordering = ("group","id",)
