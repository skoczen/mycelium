from django.template import RequestContext
from accounts.managers import get_or_404_by_account
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *

from accounts.models import AccessLevel, Account
from accounts import ACCOUNT_STATII
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def _update_account_subscription(chargify_subscription_id):
    a = Account.objects.get(chargify_subscription_id=chargify_subscription_id)
    a.update_account_status()

    return a

# @csrf_exempt
# @json_view
# def chargify_webhook(request):
#     if request.REQUEST['event'] == "subscription_state_changed":
#         for s in request.POST.getlist('payload[subscription][id]'):
#             _update_account_subscription(s)

#     return {}

