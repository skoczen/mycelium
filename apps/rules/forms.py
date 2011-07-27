# from django.forms import ModelForm, NullBooleanSelect
# from rules.models import RuleGroup

# class RuleGroupForm(ModelForm):
#     class Meta:
#         model = RuleGroup
#         fields = ("name", )

#     def __init__(self, *args, **kwargs):
#         super(RuleGroupForm, self).__init__(*args,**kwargs)
#         if self.instance.pk:
#             for i in range(self.instance.num_blank_rules,16):
#                 self.instance.make_blank_rule()
#             super(RuleGroupForm, self).__init__(*args,**kwargs)

#         