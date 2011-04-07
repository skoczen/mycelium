from django.forms import ModelForm, RadioSelect
from groups.models import Group, GroupRule
from django.forms.models import inlineformset_factory

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ("name", "rules_boolean")

class GroupRuleForm(ModelForm):
    class Meta:
        model = GroupRule
        fields = ("group", "left_side", "operator", "right_side_value" )

GroupRuleFormset = inlineformset_factory(Group, GroupRule, fields=("left_side", "operator", "right_side_value"), can_delete=True, extra=1)
