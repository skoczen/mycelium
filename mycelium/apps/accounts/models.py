from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin


class Account(TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)
