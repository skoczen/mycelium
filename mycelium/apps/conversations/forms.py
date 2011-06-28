from django.forms import ModelForm
from conversations.models import Conversation
from accounts.forms import AccountBasedModelForm
from mycelium_core.fields import JqSplitDateTimeField
from mycelium_core.widgets import JqSplitDateTimeWidget
import datetime

class NewConversationForm(AccountBasedModelForm):
    date = JqSplitDateTimeField(widget=JqSplitDateTimeWidget(attrs={'date_class':'datepicker','time_class':'timepicker'}),initial=datetime.datetime.now())
  
    class Meta:
        model = Conversation
        fields = ("account", "conversation_type", "body", "date",)
