from django.db import models
from django.utils.translation import ugettext as _

class EmailSubscription(models.Model):
    email = models.CharField(max_length=255)
    
