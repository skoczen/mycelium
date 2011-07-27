from django.forms import ModelForm, RadioSelect
from volunteers.models import CompletedShift, Volunteer
from django.forms.models import inlineformset_factory
from accounts.forms import AccountBasedModelForm

class NewShiftForm(AccountBasedModelForm):
    def __init__(self, *args, **kwargs):
        super(NewShiftForm, self).__init__(*args, **kwargs)
        self.fields["shift"].empty_label = "an unscheduled shift"
        
    class Meta:
        model = CompletedShift
        fields = ("account", "duration", "date", "shift",) #,"categories"

class VolunteerStatusForm(AccountBasedModelForm):
    def __init__(self, *args, **kwargs):
        super(VolunteerStatusForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Volunteer
        fields = ("account", "status", "reactivation_date",)
        widgets = {
            'status': RadioSelect(),
        }
