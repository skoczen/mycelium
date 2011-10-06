from django.db import models
import datetime

from qi_toolkit.models import TimestampModelMixin
from accounts.models import AccountBasedModel, UserAccount


class Activity(TimestampModelMixin):
    name            = models.CharField(max_length=255)
    points          = models.IntegerField(default=10)

    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ("name",)


class Action(AccountBasedModel, TimestampModelMixin):
    activity            = models.ForeignKey(Activity)
    staff               = models.ForeignKey(UserAccount, blank=True, null=True, on_delete=models.SET_NULL)
    staff_name          = models.CharField(max_length=255, blank=True, null=True)
    date                = models.DateTimeField(default=datetime.datetime.now())
    person              = models.ForeignKey("people.Person", blank=True, null=True)
    organization        = models.ForeignKey("organizations.Organization", blank=True, null=True)
    donation            = models.ForeignKey("donors.Donation", blank=True, null=True)
    shift               = models.ForeignKey("volunteers.CompletedShift", blank=True, null=True)
    conversation        = models.ForeignKey("conversations.Conversation", blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.staff_name:
            self.staff_name = self.staff.full_name
        
        super(Action, self).save(*args,**kwargs)

    def __unicode__(self):
        return "%s by %s on %s" % (self.activity, self.staff.full_name, self.date)
    
    class Meta:
        ordering = ("-date","-created_at")


