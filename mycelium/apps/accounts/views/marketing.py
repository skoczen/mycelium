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
from accounts.models import AccessLevel
from django.contrib.sites.models import Site


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
            return HttpResponseRedirect("%s%s.%s/" % (request.protocol, account.subdomain, site.domain))

    else:
        account_form = NewAccountForm()
        user_form = NewUserForm()

    return locals()
