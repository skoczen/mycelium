from people.models import Person
from accounts.forms import AccountBasedModelForm
import datetime


class PersonForm(AccountBasedModelForm):
    class Meta:
        model = Person
        fields = ("account", "first_name", "last_name", "email", "phone_number", "line_1", "line_2", "city", "state", "postal_code", "birth_day", "birth_month", "birth_year")

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
