from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin

class Group(SimpleSearchableModel, TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True)

    search_fields = ["name",]
    contact_type = "group"
    
    def __unicode__(self):
        return "%s" % self.name

    def searchable_name(self):
        return self.name

    class Meta(object):
        ordering = ("name",)

    def members(self):
        from people.models import Person
        if not hasattr(self,"cached_members"):
            print "Implement this!"
            self.cached_members = Person.objects.all().order_by("?")[:50]
        return self.cached_members

class GroupRule(models.Model):
    group = models.ForeignKey(Group)

    def __unicode__(self):
        return "Rule for %s" % self.group

    class Meta(object):
        ordering = ("group","id",)

