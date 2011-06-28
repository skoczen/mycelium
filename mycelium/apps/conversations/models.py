from django.db import models
from qi_toolkit.models import TimestampModelMixin
from accounts.models import AccountBasedModel
from django.core.cache import cache

from people.models import Person
from conversations import CONVERSATION_TYPES
import datetime

class Conversation(AccountBasedModel, TimestampModelMixin):
    conversation_type        = models.CharField(max_length=50, choices=CONVERSATION_TYPES, default=CONVERSATION_TYPES[0][0] )
    person                   = models.ForeignKey(Person)
    body                     = models.TextField(blank=True, null=True)
    date                     = models.DateTimeField(default=datetime.datetime.now())


    def __unicode__(self):
        return "%s on %s" % (self.conversation_type, self.date)
    
    class Meta:
        ordering = ("-date",)