from django.forms import ModelForm, RadioSelect
from groups.models import Group, GroupRule

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ("name", )

