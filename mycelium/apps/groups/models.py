from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from mycelium_core.models import SearchableItemProxy
from accounts.models import AccountBasedModel

from rules.models import Rule, RuleGroup
from people.models import Person
from django.db.models.signals import post_save, post_delete
from django.core.cache import cache
from django.template.loader import render_to_string
from mycelium_core.tasks import update_proxy_results_db_cache, put_in_cache_forever

NO_NAME_STRING_GROUP = _("Unnamed Group")

class Group(AccountBasedModel, SimpleSearchableModel, TimestampModelMixin, RuleGroup):
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
            return "%s" % self.full_name
        else:
            return ""

    class Meta(object):
        ordering = ("name",)

    @property
    def rules(self):
        return self.grouprule_set.all()

    def make_blank_rule(self):
        return self.grouprule_set.create(account=self.account)

    def num_members(self):
        return self.members.count()

    @property
    def full_name(self):
        if self.name and self.name != "":
            return "%s" % (self.name,)
        else:
            return NO_NAME_STRING_GROUP

class GroupRule(AccountBasedModel, Rule):
    group = models.ForeignKey(Group)
    
    target_model = Person

    def __unicode__(self):
        return "Rule for %s" % self.group

    class Meta(object):
        ordering = ("group","id",)


class GroupSearchProxy(SearchableItemProxy):
    SEARCH_GROUP_NAME = "groups"
    group = models.ForeignKey('groups.Group', blank=True, null=True)

    @property
    def obj(self):
        return self.group or None

    @property
    def type(self):
        if self.group_id != None:
            return "group"
        return None
    
    @property
    def obj_id(self):
        if self.group_id:
            return self.group_id            
        else:
            return None

    def get_sorting_name(self):
        sn = ""
        if self.group_id:
            sn = self.group.searchable_name
        if sn == NO_NAME_STRING_GROUP:
            sn = ""
        return sn
        
    @property
    def search_result_row(self):
        if cache.get(self.cache_name):
            return cache.get(self.cache_name)
        elif self.cached_search_result:
            put_in_cache_forever(self.cache_name,self.cached_search_result)
            return self.cached_search_result
        else:
            return self.regenerate_and_cache_search_results()

    def regenerate_and_cache_search_results(self):
        ss = self.render_result_row()
        # popping over to celery
        put_in_cache_forever(self.cache_name,ss)
        update_proxy_results_db_cache.delay(GroupSearchProxy, self,ss)
        return ss

    @property
    def cache_name(self):
        return "%s-%s-%s" % (self.search_group_name, self.type, self.obj_id)

    def generate_search_string(self):
        return self.obj.qi_simple_searchable_search_field

    def render_result_row(self):
        if self.group_id:
            return render_to_string("groups/_search_result_row_group.html",{'obj':self.obj})
        else:
            return ""

    @classmethod
    def group_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        proxy, nil = cls.raw_objects.get_or_create(account=instance.account, group=instance, search_group_name=cls.SEARCH_GROUP_NAME)
        cache.delete(proxy.cache_name)
        proxy.save()

    @classmethod
    def related_group_record_changed(cls, sender, instance, created=None, *args, **kwargs):
        cls.group_record_changed(sender, instance.group, *args, **kwargs)

    @classmethod
    def populate_cache(cls):
        [cls.group_record_changed(Group,g) for g in Group.raw_objects.all()]

    @classmethod
    def resave_all_groups(cls):
        from groups.models import Group
        [g.save() for g in Group.raw_objects.all()]


    class Meta(SearchableItemProxy.Meta):
        verbose_name_plural = "GroupSearchProxies"

    @classmethod
    def group_results_may_have_changed(cls, sender, instance, created=None, *args, **kwargs):
        from groups.tasks import regnerate_all_rulegroup_search_results_for_account
        regnerate_all_rulegroup_search_results_for_account.delay(cls, instance.account)


post_save.connect(GroupSearchProxy.group_record_changed,sender=Group)

from generic_tags.models import TaggedItem
post_save.connect(GroupSearchProxy.group_results_may_have_changed,sender=TaggedItem)
post_delete.connect(GroupSearchProxy.group_results_may_have_changed,sender=TaggedItem)

from donors.models import Donation
post_save.connect(GroupSearchProxy.group_results_may_have_changed,sender=Donation)
post_delete.connect(GroupSearchProxy.group_results_may_have_changed,sender=Donation)

from volunteers.models import CompletedShift
post_save.connect(GroupSearchProxy.group_results_may_have_changed,sender=CompletedShift)
post_delete.connect(GroupSearchProxy.group_results_may_have_changed,sender=CompletedShift)
