from django.forms import ModelForm
from conversations.models import Conversation
from accounts.forms import AccountBasedModelForm
from mycelium_core.fields import JqSplitDateTimeField
from mycelium_core.widgets import JqSplitDateTimeWidget
# import datetime
from timezones.utils import datetime

class NewConversationForm(AccountBasedModelForm):
    date = JqSplitDateTimeField(widget=JqSplitDateTimeWidget(attrs={'date_class':'datepicker','time_class':'timepicker'}))
  
    class Meta:
        model = Conversation
        fields = ("account", "conversation_type", "body", "staff", "date",)

    def __init__(self, *args, **kwargs):
        print args
        super(NewConversationForm,self).__init__(*args,**kwargs)
        self.fields["staff"].choices = [i for i in self.fields["staff"].choices][1:]
        now = datetime.now()
        self.fields["date"].initial = now

