from django.db import models
from qi_toolkit.models import TimestampModelMixin
from accounts.models import AccountBasedModel
from django.core.cache import cache
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from people.models import Person
from accounts.models import UserAccount
from conversations import CONVERSATION_TYPES, GIST_LENGTH
import datetime



class Conversation(AccountBasedModel, TimestampModelMixin):
    conversation_type        = models.CharField(max_length=50, choices=CONVERSATION_TYPES, default=CONVERSATION_TYPES[0][0] )
    person                   = models.ForeignKey(Person)
    staff                    = models.ForeignKey(UserAccount)
    body                     = models.TextField(blank=True, null=True)
    date                     = models.DateTimeField(default=datetime.datetime.now())


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