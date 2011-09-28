from django.forms import ModelForm
from donors.models import Donation
from accounts.forms import AccountBasedModelForm

class NewDonationForm(AccountBasedModelForm):
  
    class Meta:
        model = Donation
        fields = ("account", "amount", "date", "type", "notes")
