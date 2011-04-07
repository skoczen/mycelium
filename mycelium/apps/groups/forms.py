from django.forms import ModelForm, RadioSelect, HiddenInput, TextInput, Select, NullBooleanSelect
from groups.models import Group, GroupRule
from django.forms.models import inlineformset_factory

class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = ("name", "rules_boolean")
        widgets = {
            'rules_boolean': NullBooleanSelect()
        }

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args,**kwargs)
        self.fields['rules_boolean'].widget.choices = [("2", "all"), ("3","any")]

class GroupRuleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GroupRuleForm, self).__init__(*args,**kwargs)
        self.fields["right_side_value"].widget=TextInput()
        if self.instance.right_side_type:
            if self.instance.right_side_type.name == "text":
                self.fields["right_side_value"].widget=TextInput()
                # self.fields["right_side_value"].initial=self.instance.right_side_value
            elif self.instance.right_side_type.name == "date":
                self.fields["right_side_value"].widget=TextInput()
                # self.fields["right_side_value"].initial=self.instance.right_side_value
            elif self.instance.right_side_type.name == "choices":
                self.fields["right_side_value"].widget=Select()
                # self.fields["right_side_value"].initial=self.instance.right_side_value
        
        self.fields["right_side_type"].widget=HiddenInput()
        # self.fields["right_side_type"].initial=self.instance.right_side_type

        
    class Meta:
        model = GroupRule
        

GroupRuleFormset = inlineformset_factory(Group, GroupRule, fields=("left_side", "operator", "right_side_value", "right_side_type" ), can_delete=True, extra=1, form=GroupRuleForm)
