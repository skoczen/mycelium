from django.template import RequestContext
from django.shortcuts import render_to_response
from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from accounts.forms import NewAccountForm, NewUserForm
from accounts.models import AccessLevel, Account
from accounts.tasks import send_welcome_emails
from django.contrib.sites.models import Site
from django.conf import settings
from pychargify.api import *

@render_to("accounts/signup.html")
def signup(request):
    
    if request.method == "POST":
        account_form = NewAccountForm(request.POST)
        user_form = NewUserForm(request.POST)
        if account_form.is_valid() and user_form.is_valid():
            account = account_form.save()
            useraccount = account.create_useraccount(full_name=user_form.cleaned_data['first_name'], 
                                       username=user_form.cleaned_data['username'], 
                                       password=user_form.cleaned_data['password'], 
                                       email=user_form.cleaned_data['email'], 
                                       access_level=AccessLevel.admin()
                                       )
            site = Site.objects.get_current()

            # Send off emails to us and them.
            send_welcome_emails.delay(account, useraccount)

            return HttpResponseRedirect("%s%s.%s/" % (request.protocol, account.subdomain, site.domain))
        else:
            # print account_form
            # print user_form
            pass
    else:
        account_form = NewAccountForm()
        user_form = NewUserForm()

    return locals()

@json_view
def verify_subdomain(request):
    is_available = False
    if request.method == "POST" and "subdomain" in request.POST:
        is_available = Account.objects.filter(subdomain=request.POST["subdomain"]).count() == 0
    
    return {'success':True, 'is_available':is_available}



@json_view
def chargify_webhook(request):
    print request.POST
    # billing_subscription_id = request.GET['subscription_id']
    # billing_customer_id = request.GET['customer_id']
    # account_id = request.GET['account_id']

    # go to the chargify API, and verify the status.
    chargify = Chargify(settings.CHARGIFY_API, settings.CHARGIFY_SUBDOMAIN)
    # chargify_customer = chargify.Customer(id=billing_customer_id)
    print chargify


    # a = Account.objects.get(pk=account_id)
    # a.subscription_id
    return {}