from django.db import models
from qi_toolkit.models import TimestampModelMixin
from accounts.models import AccountBasedModel
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from people.models import Person
from accounts.models import UserAccount
from conversations import CONVERSATION_TYPES, GIST_LENGTH
import datetime



class Conversation(AccountBasedModel, TimestampModelMixin):
    conversation_type        = models.CharField(max_length=50, choices=CONVERSATION_TYPES, default=CONVERSATION_TYPES[0][0] )
    person                   = models.ForeignKey(Person)
    staff                    = models.ForeignKey(UserAccount, blank=True, null=True, on_delete=models.SET_NULL)
    staff_name               = models.CharField(max_length=255, blank=True, null=True)
    body                     = models.TextField(blank=True, null=True)
    date                     = models.DateTimeField(default=datetime.datetime.now())


    def save(self, *args, **kwargs):
        if not self.staff_name:
            self.staff_name = self.staff.full_name
        super(Conversation, self).save(*args,**kwargs)

    def __unicode__(self):
        return "%s on %s" % (self.conversation_type, self.date)
    
    class Meta:
        ordering = ("-date","-created_at")

    @property
    def bigger_than_the_gist(self):
        return len(self.body) > GIST_LENGTH

    @property
    def gist(self):
        if self.bigger_than_the_gist:
            return self.body[:GIST_LENGTH]
        else:
            return self.body
    
    @property
    def gist_with_elipsis(self):
        if self.bigger_than_the_gist:
            return "%s..." % self.gist
        else:
            return self.gist

    @property
    def remainder(self):
        if self.bigger_than_the_gist:
            return self.body[GIST_LENGTH:]
        else:
            return self.body    

    @property
    def body_with_see_more_link(self):
        return mark_safe(render_to_string("conversations/_conversation_with_see_more_link.html", {'conversation':self}))

    @property
    def staff_nickname_or_full_name(self):
        if not self.staff:
            return self.staff_name
        else:
            return self.staff.nickname_or_full_name