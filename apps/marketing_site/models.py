from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from django.contrib.auth.models import User

class GoodCloudEmployee(TimestampModelMixin):
    user = models.ForeignKey(User)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True, max_length=255)
    picture = models.ImageField(blank=True, null=True, upload_to="_goodcloud_people")

    @property
    def full_name(self):
        return "%s %s" % (self.user.first_name, self.user.last_name,)

    def __unicode__(self):
        return self.full_name
        
    class Meta(object):
        ordering = ("user__first_name","user__last_name")