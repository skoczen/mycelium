from django.db import models
from django.utils.translation import ugettext as _

# Make the username field 100 chars long
from django.db.models.signals import class_prepared

def longer_username(sender, *args, **kwargs):
    # You can't just do `if sender == django.contrib.auth.models.User`
    # because you would have to import the model
    # You have to test using __name__ and __module__
    if sender.__name__ == "User" and sender.__module__ == "django.contrib.auth.models":
        sender._meta.get_field("username").max_length = 100
        sender._meta.get_field("username").help_text = _("Required. Only letters, numbers, and @, ., +, -, or _ characters.")

class_prepared.connect(longer_username)