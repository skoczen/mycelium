from django.forms import ModelForm
from volunteers.models import VolunteerShift
from django.forms.models import inlineformset_factory

class NewShiftForm(ModelForm):
    class Meta:
        model = VolunteerShift
        fields = ("time", "date", "event", "categories",)
