from django.forms import *
from logo_maker.models import Logo
from accounts.forms import AccountBasedModelForm

class LogoForm(AccountBasedModelForm):
    class Meta:
        model = Logo
        fields = ("account", "name", "image")
