from django.forms import ModelForm, RadioSelect
from generic_tags.models import TagSet
from taggit.models import Tag

class TagSetForm(ModelForm):
    class Meta:
        model = TagSet
        fields = ("name", )

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ("name", )

