from django.forms import ModelForm, RadioSelect, HiddenInput, TextInput, Select, NullBooleanSelect
from groups.models import Group, GroupRule
from django.forms.models import inlineformset_factory, BaseModelFormSet, BaseInlineFormSet
from accounts.forms import AccountBasedModelForm, adjust_queryset_for_account_based_models, AccountBasedModelFormSet


class GroupForm(AccountBasedModelForm):
    class Meta:
        model = Group
        fields = ("account", "name", "rules_boolean")
        widgets = {
            'rules_boolean': NullBooleanSelect()
        }

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args,**kwargs)
        if self.instance.pk:
            for i in range(self.instance.num_blank_rules,16):
                self.instance.make_blank_rule()
            super(GroupForm, self).__init__(*args,**kwargs)

        
        self.fields['rules_boolean'].widget.choices = [("2", "all"), ("3","any")]


class GroupRuleForm(AccountBasedModelForm):
    def __init__(self, *args, **kwargs):
        super(GroupRuleForm, self).__init__(*args,**kwargs)
        self.fields["right_side_value"].widget=TextInput()
        self.fields["right_side_type"].widget=HiddenInput()

    class Meta:
        model = GroupRule
        fields = ("account", "left_side", "operator", "right_side_type", "right_side_value", "group")

class GroupRuleFormsetBase(AccountBasedModelFormSet):
    def save_existing_objects(self, *args, **kwargs):
        from django.core.exceptions import ValidationError
        for f in self.initial_forms:
            if f.fields["DELETE"].clean(f._raw_value("DELETE")):
                try:
                    f.fields["id"].clean(f._raw_value("id"))
                except ValidationError:
                    del self.forms[self.forms.index(f)]

        return super(GroupRuleFormsetBase, self).save_existing_objects(*args, **kwargs)


GroupRuleFormset = inlineformset_factory(Group, GroupRule, fields=("left_side", "operator", "right_side_value", "right_side_type" ), can_delete=True, extra=0, form=GroupRuleForm, formset=GroupRuleFormsetBase )