from django.forms import ModelForm
from conversations.models import Conversation
from accounts.forms import AccountBasedModelForm

class NewConversationForm(AccountBasedModelForm):
  
    class Meta:
        model = Conversation
        fields = ("account", "conversation_type", "body", "date",)
