from taggit.managers import TaggableManager, _TaggableManager
from qi_toolkit.monkeypatch import monkeypatch_method, monkeypatch_class


# @monkeypatch_method(_TaggableManager)
# def all_tags_of_my_type(self):
#     return self.through.tag_model().objects.all()

# @monkeypatch_method(_TaggableManager)
# def all_tags_of_my_type_alphabetical_by_name(self):
#     return self.through.tag_model().objects.order_by("name").all()

# @monkeypatch_method(_TaggableManager)
# def alphabetical_by_name(self):
#     return self.all().order_by("name")



class _GenericTagsTaggableManager(_TaggableManager):
    __metaclass__ = monkeypatch_class
    
    def all_tags_of_my_type(self):
        return self.all()

    def all_tags_of_my_type_alphabetical_by_name(self):
        return self.order_by("name").all()

    def alphabetical_by_name(self):
        return self.all().order_by("name")


class GenericTagsTaggableManager(TaggableManager):
    __metaclass__ = monkeypatch_class

    # Using Taggit entirely, and adding a few classes.
    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError("%s objects need to have a primary key value "
                "before you can access their tags." % model.__name__)
        manager = _GenericTagsTaggableManager(
            through=self.through, model=model, instance=instance
        )
        return manager
