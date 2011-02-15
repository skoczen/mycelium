from django.forms import ModelForm, RadioSelect
from people.models import Person, EmailAddress, PhoneNumber, Address, Organization

class PersonForm(ModelForm):
    class Meta:
        model = Person
        fields = ("first_name", "last_name")


class EmailForm(ModelForm):
    class Meta:
        model = EmailAddress
        fields = ("email",)

class PhoneForm(ModelForm):
    class Meta:
        model = PhoneNumber
        fields = ("phone_number",)

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ("line_1", "line_2", "city", "state", "postal_code",)
        
class OrganizationForm(ModelForm):
    # def __init__(self, *args,**kwargs):
    #     super(OrganizationForm,self).init(*args,**kwargs)
    #     self.fields['organization_type'].__dict__

    class Meta:
        model = Organization
        fields = ("name", "primary_phone_number", "website", "twitter_username", "line_1", "line_2", "city", "state", "postal_code",)
        # fields += ("organization_type", "organization_type_other_name",)
        # widgets = { 'organization_type': RadioSelect(), }