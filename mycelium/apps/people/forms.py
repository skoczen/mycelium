from django.forms import ModelForm, RadioSelect
from people.models import Person, Organization, Employee
from django.forms.models import inlineformset_factory
# EmailAddress, PhoneNumber, Address

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ("first_name", "last_name", "email", "phone_number", "line_1", "line_2", "city", "state", "postal_code",)


# class EmailForm(ModelForm):
#     class Meta:
#         model = EmailAddress
#         fields = ("email",)
# 
# class PhoneForm(ModelForm):
#     class Meta:
#         model = PhoneNumber
#         fields = ("phone_number",)
# 
# class AddressForm(ModelForm):
#     class Meta:
#         model = Address
#         fields = ("line_1", "line_2", "city", "state", "postal_code",)
        
class OrganizationForm(ModelForm):
    # def __init__(self, *args,**kwargs):
    #     super(OrganizationForm,self).init(*args,**kwargs)
    #     self.fields['organization_type'].__dict__

    class Meta:
        model = Organization
        fields = ("name", "primary_phone_number", "website", "twitter_username", "line_1", "line_2", "city", "state", "postal_code",)
        # fields += ("organization_type", "organization_type_other_name",)
        # widgets = { 'organization_type': RadioSelect(), }
        
class PersonViaOrganizationForm(ModelForm):
    class Meta:
        model = Person
        fields = ("first_name", "last_name")

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ("role", "email", "phone_number")

EmployeeFormset = inlineformset_factory(Person, Employee, fields=("role", "email", "phone_number"), can_delete=False, extra=0)
EmployeeFormsetFromOrg = inlineformset_factory(Organization, Employee, fields=("role", "email", "phone_number"), can_delete=False, extra=0)