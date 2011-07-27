from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import TimestampModelMixin
from accounts.models import AccountBasedModel

class Logo(AccountBasedModel, TimestampModelMixin):
    image = models.ImageField(upload_to="_logos")
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % (self.name)
