from django.forms import ModelForm
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
    class Meta:
        model = Organization
        fields = ("name", "organization_type", "organization_type_other_name", "primary_phone_number", "website", "twitter_username", "line_1", "line_2", "city", "state", "postal_code",)
