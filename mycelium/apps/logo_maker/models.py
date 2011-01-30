from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import TimestampModelMixin

class Logo(TimestampModelMixin):
    image = models.ImageField(upload_to="logos")
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % (self.name)
