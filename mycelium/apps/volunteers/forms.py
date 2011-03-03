from django.forms import ModelForm
from volunteers.models import CompletedShift
from django.forms.models import inlineformset_factory

class NewShiftForm(ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(NewShiftForm, self).__init__(*args, **kwargs)
    #     self.fields["completed"].initial = True
        
    class Meta:
        model = CompletedShift
        fields = ("duration", "date", "shift",) #,"categories"
