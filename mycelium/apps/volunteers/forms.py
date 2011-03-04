from django.forms import ModelForm
from volunteers.models import CompletedShift
from django.forms.models import inlineformset_factory

class NewShiftForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewShiftForm, self).__init__(*args, **kwargs)
        print self.fields["shift"].__dict__
        self.fields["shift"].empty_label = "an unscheduled shift"
        
    class Meta:
        model = CompletedShift
        fields = ("duration", "date", "shift",) #,"categories"
