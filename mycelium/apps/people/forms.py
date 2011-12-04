import datetime

from django.forms.models import inlineformset_factory

from accounts.forms import AccountBasedModelForm, AccountBasedModelFormSet
from people.models import Person, PersonPhoneNumber, PersonEmailAddress

class PersonForm(AccountBasedModelForm):
    class Meta:
        model = Person
        fields = ("account", "first_name", "last_name", "line_1", "line_2", "city", "state", "postal_code", "birth_day", "birth_month", "birth_year")

    def __init__(self, *args, **kwargs):
        super(PersonForm,self).__init__(*args,**kwargs)
        self.fields["birth_month"].choices = [("","Unknown")] + [i for i in self.fields["birth_month"].choices][1:]

    def clean(self, *args,**kwargs):
        super(PersonForm,self).clean(*args,**kwargs)
        if self.cleaned_data["birth_month"] and self.cleaned_data["birth_day"]:
            # make sure they're valid.
            try:
                year = 1980
                if self.cleaned_data["birth_year"]:
                    year = self.cleaned_data["birth_year"]

                datetime.date(month=self.cleaned_data["birth_month"], day=self.cleaned_data["birth_day"], year=year)
            except:
                self.cleaned_data["birth_month"] = None
                self.cleaned_data["birth_day"] = None

        return self.cleaned_data

class PhoneNumberForm(AccountBasedModelForm):
    class Meta:
        model = PersonPhoneNumber
        fields = ("phone_number", "contact_type", "primary")


class EmailAddressForm(AccountBasedModelForm):
    class Meta:
        model = PersonEmailAddress
        fields = ("email", "contact_type", "primary")


PhoneNumberFormset = inlineformset_factory(Person,
                             PersonPhoneNumber, 
                             fields=("account", "phone_number", "contact_type", "primary"), 
                             can_delete=True, 
                             extra=0, 
                             form=PhoneNumberForm, 
                             formset=AccountBasedModelFormSet
                    )



EmailAddressFormset = inlineformset_factory(Person,
                             PersonEmailAddress, 
                             fields=("account", "email", "contact_type", "primary"), 
                             can_delete=True, 
                             extra=0, 
                             form=EmailAddressForm, 
                             formset=AccountBasedModelFormSet
                    )

