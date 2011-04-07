from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from people.models import NO_NAME_STRING

from rules.models import Rule, RuleGroup
from people.models import Person

class Group(SimpleSearchableModel, TimestampModelMixin, RuleGroup):
    name = models.CharField(max_length=255, blank=True, null=True)

    # include_people = models.BooleanField(default=True)
    # include_organizations = models.BooleanField(default=False)
    # include_groups = models.BooleanField(default=False)

    target_model = Person

    search_fields = ["name",]
    contact_type = "group"
    
    def __unicode__(self):
        return "%s" % self.name

    @property
    def searchable_name(self):
        if self.name:
            return "%s" % self.name
        else:
            return ""

    class Meta(object):
        ordering = ("name",)

    @property
    def rules(self):
        return self.grouprule_set.all()


    @property
    def full_name(self):
        if self.name and self.name != "":
            return "%s" % (self.name,)
        else:
            return NO_NAME_STRING

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