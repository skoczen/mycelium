from django.forms import ModelForm, RadioSelect
from generic_tags.models import TagSet

class TagSetForm(ModelForm):
    class Meta:
        model = TagSet
        fields = ("name", )

