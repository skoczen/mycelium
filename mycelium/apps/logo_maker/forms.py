from django.forms import *
from logo_maker.models import Logo

class LogoForm(ModelForm):
    class Meta:
        model = Logo
        fields = ("name", "image")
