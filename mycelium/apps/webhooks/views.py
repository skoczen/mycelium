from django.template import RequestContext
from accounts.managers import get_or_404_by_account
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *

from accounts.models import AccessLevel, Account
from accounts import CHARGIFY_STATUS_MAPPING, ACCOUNT_STATII
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

def _update_account_subscription(account_id, chargify_subscription_id):
    a = Account.objects.get(pk=account_id)
    a.chargify_subscription_id = chargify_subscription_id
    a.save()

    a.update_account_status()
    return a

@json_view
@csrf_exempt
def chargify_webhook(request):
    assert request.POST['event'][0] == "subscription_state_change"
    
    payload = request.POST['payload']

    account_id = payload["customer_reference"]
    subscription_id = payload["subscription_id"]
    account = _update_account_subscription(account_id, subscription_id)
    return {}

@csrf_exempt
@render_to("webhooks/chargify_postback.html")
def chargify_postback(request):
    chargify_subscription_id = request.GET['subscription_id']
    account_id = request.GET['customer_reference']
    account = _update_account_subscription(account_id, chargify_subscription_id)

    # redirect to their account page.
    return locals()
    # return HttpResponseRedirect("%s%s.%s/accounts/manage-account" % (request.protocol, account.subdomain, "agoodcloud.com"))
    