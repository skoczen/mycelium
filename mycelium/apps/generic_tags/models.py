from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from django.db.models.signals import post_save
import datetime
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^generic_tags\.manager.TaggableManager"])


class TagSet(TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)


    # @property
    # def groups(self):
    #     return Group.objects.filter(id__in=self.groupmembership_set.values("group_id")).all()


    # def add_tag(self, person, name):
    #     tsm = self.tagsetmembership_set.filter(person=person).tags()
    #     group = Group.objects.filter(name__iexact=name).all()
    #     if group.count() == 1:
    #         group = group[0]
    #     elif group.count() == 0:
    #         group = Group.objects.create(name=name)[0]
    #     else:
    #         raise Exception, "More than one group with this name!"
        
    #     return self.groupmembership_set.get_or_create(group=group)

    # def remove_group(self, name):
    #     try:
    #         group = Group.objects.get(name__iexact=name)
    #         gm = self.groupmembership_set.get(group=group)
    #         gm.delete()
    #     except:
    #         pass


class TagSetMembership(TimestampModelMixin):
    tagset = models.ForeignKey(TagSet, blank=True, null=True)
    person = models.ForeignKey('people.Person', blank=True, null=True)

    tags = TaggableManager()

    def __unicode__(self):
        return "%s in %s" % (self.tagset, self.person)

    class Meta(object):
        ordering = ("tagset","person",)