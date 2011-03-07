from django.forms import ModelForm, RadioSelect
from volunteers.models import CompletedShift, Volunteer
from django.forms.models import inlineformset_factory

class NewShiftForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewShiftForm, self).__init__(*args, **kwargs)
        self.fields["shift"].empty_label = "an unscheduled shift"
        
    class Meta:
        model = CompletedShift
        fields = ("duration", "date", "shift",) #,"categories"

class VolunteerStatusForm(ModelForm):
    class Meta:
        model = Volunteer
        fields = ("status", "reactivation_date",)
        widgets = {
            'status': RadioSelect(),
        }
