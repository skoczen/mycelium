from django.forms import ModelForm
from donors.models import Donation

class NewDonationForm(ModelForm):
  
    class Meta:
        model = Donation
        fields = ("amount", "date",)
