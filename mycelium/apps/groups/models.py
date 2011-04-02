from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from people.models import NO_NAME_STRING

from rules.models import Rule

class Group(SimpleSearchableModel, TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True)

    # include_people = models.BooleanField(default=True)
    # include_organizations = models.BooleanField(default=False)
    # include_groups = models.BooleanField(default=False)
    # rules_boolean = models.BooleanField() # True==All  False==Any

    search_fields = ["name",]
    contact_type = "group"
    
    def __unicode__(self):
        return "%s" % self.name

    @property
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


    @property
    def full_name(self):
        if self.name:
            return "%s" % (self.name,)
        else:
            return NO_NAME_STRING

from people.models import Person
class GroupRule(Rule):
    group = models.ForeignKey(Group)
    
    target_model = Person

    def __unicode__(self):
        return "Rule for %s" % self.group

    class Meta(object):
        ordering = ("group","id",)

from django.db.models.signals import post_save
from people.models import PeopleAndOrganizationsSearchProxy
post_save.connect(PeopleAndOrganizationsSearchProxy.group_record_changed,sender=Group)