from django.template import RequestContext
from accounts.managers import get_or_404_by_account
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *

from accounts.models import AccessLevel, Account

from django.conf import settings
from pychargify.api import *
from django.views.decorators.csrf import csrf_exempt

def _update_account_subscription(account_id, chargify_subscription_id):
    # go to the chargify API, and verify the status.
    chargify = ChargifySubscription(settings.CHARGIFY_API, settings.CHARGIFY_SUBDOMAIN)
    chargify_sub = chargify.getBySubscriptionId(chargify_subscription_id)

    print chargify_sub
    print chargify_sub.__dict__
    print chargify_sub.activated_at
    print chargify_sub.state
    print chargify_sub.cancel_at_end_of_period
    print chargify_sub.next_assessment_at
    print chargify_sub.customer.__dict__
    print chargify_sub.product.__dict__

    a = Account.objects.get(pk=account_id)
    print a
    
    return a

@json_view
@csrf_exempt
def chargify(request):
    print request.POST
    # assert request.POST['event'][0] == "subscription_state_change"
    # May be subscription_state_change
    # or signup_success
    # the others we don't care about.

    payload = request.POST['payload']
    print payload

    account_id = payload["customer_reference"]
    subscription_id = payload["subscription_id"]
    account = _update_account_subscription(account_id, subscription_id)    
    return {}

@csrf_exempt
def chargify_postback(request):
    chargify_subscription_id = request.GET['subscription_id']
    account_id = request.GET['customer_reference']
    account = _update_account_subscription(account_id, chargify_subscription_id)

    # redirect to their account page.
    print    HttpResponseRedirect("%s%s.%s/accounts/manage-account" % (request.protocol, account.subdomain, "agoodcloud.com"))
    # return HttpResponseRedirect("%s%s.%s/accounts/manage-account" % (request.protocol, account.subdomain, "agoodcloud.com"))
    return {}