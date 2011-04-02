from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from django.db.models.signals import post_save
import datetime
from taggit.managers import TaggableManager
from taggit.models import TaggedItem, Tag

from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^generic_tags\.manager.TaggableManager"])
from django.template.defaultfilters import slugify

class TagSet(TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    slug = models.SlugField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(TagSet,self).save(*args, **kwargs)

    class Meta(object):
        ordering = ("id",)

    @property
    def all_tags(self):
        """Returns all tags possible in this set"""
        # Should be cached, most likely.

        # Needs to be a queryset, for the other options to like it.
        from django.contrib.contenttypes.models import ContentType
        tsm_ct = ContentType.objects.get_for_model(TagSetMembership)
        tsms = self.tagsetmembership_set.all()
        
        all_tags = Tag.objects.filter(pk__in=TaggedItem.objects.filter(content_type=tsm_ct, object_id__in=tsms).values("tag").distinct()).order_by("name")

        return all_tags

        # Needs clear definition on what it's returning. Do this tomorrow.
        raise Exception, "Not Implemented yet"

    @property
    def form(self, *args, **kwargs):
        from generic_tags.forms import TagSetForm
        return TagSetForm(*args, instance=self, **kwargs)

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

    @property
    def all_tags_with_my_tags_marked(self):
        my_tags = self.tags.all()
        all_tags = self.tagset.all_tags
        combined_tags = []
        for at in all_tags:
            has_tag = at in my_tags
            combined_tags.append({'has_tag':has_tag,'tag':at})

        return combined_tags

    def __unicode__(self):
        return "%s in %s" % (self.tagset, self.person)

    class Meta(object):
        ordering = ("tagset","person",)

from rules.tasks import populate_rule_components
post_save.connect(populate_rule_components,sender=TagSet)