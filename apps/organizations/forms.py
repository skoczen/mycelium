from django.forms import ModelForm, RadioSelect
from people.models import Person 
from organizations.models import Organization, Employee
from django.forms.models import inlineformset_factory
from accounts.forms import AccountBasedModelForm, AccountBasedModelFormSet
        
class OrganizationForm(AccountBasedModelForm):
    # def __init__(self, *args,**kwargs):
    #     super(OrganizationForm,self).init(*args,**kwargs)
    #     self.fields['organization_type'].__dict__

    class Meta:
        model = Organization
        fields = ("account", "name", "primary_phone_number", "website", "twitter_username", "line_1", "line_2", "city", "state", "postal_code",)
        # fields += ("organization_type", "organization_type_other_name",)
        # widgets = { 'organization_type': RadioSelect(), }
        
class PersonViaOrganizationForm(AccountBasedModelForm):
    class Meta:
        model = Person
        fields = ("account", "first_name", "last_name")

class EmployeeForm(AccountBasedModelForm):
    class Meta:
        model = Employee
        fields = ("account", "role", "email", "phone_number")

EmployeeFormset = inlineformset_factory(Person, Employee, fields=("account", "role", "email", "phone_number"), can_delete=False, extra=0, form=EmployeeForm, formset=AccountBasedModelFormSet)
EmployeeFormsetFromOrg = inlineformset_factory(Organization, Employee, fields=("account", "role", "email", "phone_number"), can_delete=False, extra=0, form=EmployeeForm, formset=AccountBasedModelFormSet)