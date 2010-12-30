from django.forms import ModelForm
from people.models import Person, EmailAddress, PhoneNumber, Address

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