from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from django.db.models.signals import post_save, post_delete
from django.template.defaultfilters import slugify

from south.modelsinspector import add_ignored_fields
add_ignored_fields(["^generic_tags\.manager.TaggableManager"])

from generic_tags import BLANK_TAGSET_NAME

from accounts.models import AccountBasedModel

class TagSet(AccountBasedModel, TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        if self.name == None or self.name == "":
            self.name = BLANK_TAGSET_NAME

        self.slug = slugify(self.name)
        super(TagSet,self).save(*args, **kwargs)

    class Meta(object):
        ordering = ("id",)

    @property
    def all_tags(self):
        """Returns all tags possible in this set"""
        # Should be cached, most likely.
        if not hasattr(self, "cached_all_tags"):
            self.cached_all_tags = self.tag_set.all()

        return self.cached_all_tags

    @property
    def all_tags_and_counts_with_form(self):
        # TODO Should also be cached.
        if not hasattr(self, "cached_all_tags_and_counts"):
            self.cached_all_tags_and_counts = []
            for t in self.all_tags:
                self.cached_all_tags_and_counts.append({
                    'tag':t,
                    'num_people': TaggedItem.objects_by_account(self.account).filter(tag=t.id).count(),
                })

        return self.cached_all_tags_and_counts

    
    def all_tags_with_users_tags_marked(self, person):
        # ghetto caching
        if not hasattr(self, "cached_all_tags_with_users_tags_marked"):
            my_tags = person.taggeditem_set.values_list("tag",flat=True)
            self.cached_all_tags_with_users_tags_marked = []
            for at in self.all_tags:
                has_tag = at.pk in my_tags
                self.cached_all_tags_with_users_tags_marked.append({'has_tag':has_tag,'tag':at})

        return self.cached_all_tags_with_users_tags_marked


    def form(self, *args, **kwargs):
        from generic_tags.forms import TagSetForm
        form_context = {'instance':self, 'prefix':"TAGSET-%s" % self.pk}
        form_context.update(**kwargs)
        return TagSetForm(*args, **form_context)

    

class Tag(AccountBasedModel, models.Model):
    name = models.CharField(verbose_name=_('Name'), max_length=250)
    slug = models.SlugField(verbose_name=_('Slug'), max_length=255)
    tagset = models.ForeignKey(TagSet, blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta(object):
        ordering = ("tagset","name",)


    def form(self, *args, **kwargs):
        from generic_tags.forms import TagForm
        form_context = {'instance':self, 'prefix':"TAG-%s" % self.pk}
        form_context.update(**kwargs)
        return TagForm(*args, **form_context)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)
        return super(Tag, self).save(*args, **kwargs)


    def add_tag_to_person(self, person=None):
        if not person:
            raise Exception, "Missing person"
        return TaggedItem.raw_objects.get_or_create(account=person.account, tag=self, person=person)[0]

    def remove_tag_from_person(self, person=None):
        if not person:
            raise Exception, "Missing person"
        TaggedItem.objects_by_account(self.account).filter(tag=self, person=person).delete()

    @classmethod
    def create_new_tag(cls, tagset=None, name=None):
        if not tagset or not name:
            raise Exception, "Missing tagset and/or name"
        return cls.raw_objects.get_or_create(tagset=tagset, name=name)[0]

class TaggedItem(AccountBasedModel, models.Model):
    tag = models.ForeignKey(Tag)
    person = models.ForeignKey('people.Person', blank=True, null=True)

    def __unicode__(self):
        return "%s tag for %s" % (self.tag, self.person)

    class Meta(object):
        ordering = ("tag","person",)



from rules.tasks import populate_rule_components_for_an_obj_with_an_account_signal_receiver
post_save.connect(populate_rule_components_for_an_obj_with_an_account_signal_receiver,sender=TagSet)
post_delete.connect(populate_rule_components_for_an_obj_with_an_account_signal_receiver,sender=TagSet)