from django.forms import ModelForm, RadioSelect
from generic_tags.models import TagSet, Tag
from accounts.forms import AccountBasedModelForm

class TagSetForm(AccountBasedModelForm):
    class Meta:
        model = TagSet
        fields = ("account", "name", )

class TagForm(AccountBasedModelForm):
    class Meta:
        model = Tag
        fields = ("account", "name", )

