from django import forms
from email_list.models import EmailSubscription

class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailSubscription
        fields = ("email",)

