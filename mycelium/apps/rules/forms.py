from django.forms import ModelForm, NullBooleanSelect
from rules.models import Rule

class RuleGroupForm(ModelForm):
    class Meta:
        model = Rule
        fields = ("name", "rules_boolean")
        widgets = {
            'rules_boolean': NullBooleanSelect()
        }

    def __init__(self, *args, **kwargs):
        super(RuleGroupForm, self).__init__(*args,**kwargs)
        if self.instance.pk:
            for i in range(self.instance.num_blank_rules,16):
                self.instance.make_blank_rule()
            super(RuleGroupForm, self).__init__(*args,**kwargs)
            
        self.fields['rules_boolean'].widget.choices = [("2", "all"), ("3","any")]
        