# This is ripped directly from django's contrib.auth.views, but has been modified to pass the request on to the form consistently.
import re
from django.conf import settings
from django.contrib.auth import REDIRECT_FIELD_NAME
# Avoid shadowing the login() view below.
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.sites.models import get_current_site
from zebra.forms import StripePaymentForm
import stripe


from qi_toolkit.helpers import *
from accounts.forms import UserAccountAccessFormset, NewUserAccountForm, AccountForm, UserFormForUserAccount, UserAccountNicknameForm
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from accounts.models import UserAccount


@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):
    """Displays the login form and handles the login action."""
    

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST, auth_request=request)
        print form
        print form.is_valid()
        if form.is_valid():
            # Light security check -- make sure redirect_to isn't garbage.
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- redirects to http://example.com should
            # not be allowed, but things like /view/?param=http://example.com
            # should be allowed. This regex checks if there is a '//' *before* a
            # question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                    redirect_to = settings.LOGIN_REDIRECT_URL

            # Okay, security checks complete. Log the user in.
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            
            request.session.modified = True
            return HttpResponseRedirect(redirect_to)

    else:
        request.session.clear()
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))


def _account_forms(request):
    data = None
    if request.method == "POST":
        data = request.POST

    user_access_formset = UserAccountAccessFormset(data,instance=request.account)
    new_user_form = NewUserAccountForm(data)
    return user_access_formset, new_user_form

@render_to("accounts/manage_users.html")
def manage_users(request):
    section = "admin"
    if not request.useraccount.is_admin:
        return HttpResponseRedirect(reverse("dashboard:dashboard"))

    user_access_formset, new_user_form = _account_forms(request)
    return locals()

@json_view
def save_account_access_info(request):
    success = False

    user_access_formset, new_user_form = _account_forms(request)
    if user_access_formset.is_valid():
        user_access_formset.save()
    
    return {"success":success}

@json_view
def reset_account_password(request, ua_id):
    success = False

    ua = UserAccount.objects.get(account=request.account, pk=ua_id)
    user = ua.user
    user.set_password("changeme!")
    user.save()

    return {"success":success}

def delete_account(request, ua_id):
    ua = UserAccount.objects.get(account=request.account, pk=ua_id)
    user = ua.user
    user.delete()
    ua.delete()
    return HttpResponseRedirect(reverse("accounts:manage_users"))    

# @json_view
def save_new_account(request):
    success = False
    if request.method == "POST":
        new_user_form = NewUserAccountForm(request.POST)

        if new_user_form.is_valid():
            request.account.create_useraccount(
                                       full_name=new_user_form.cleaned_data['first_name'], 
                                       username=new_user_form.cleaned_data['username'], 
                                       password=new_user_form.cleaned_data['password'], 
                                       email=new_user_form.cleaned_data['email'], 
                                       access_level=new_user_form.cleaned_data['access_level']
                                       )
    
    # return {"success":success}
    return HttpResponseRedirect(reverse("accounts:manage_users"))


def dashboard(request):
    return HttpResponseRedirect(reverse("dashboard:dashboard"))

@render_to("accounts/manage_account.html")
def manage_account(request):
    section = "admin"
    STRIPE_PUBLISHABLE = settings.STRIPE_PUBLISHABLE

    form = AccountForm(instance=request.account)

    if request.method == 'POST':
        zebra_form = StripePaymentForm(request.POST)
        if zebra_form.is_valid():
            customer = request.account.stripe_customer
            customer.card = zebra_form.cleaned_data['stripe_token']
            customer.save()

            account = request.account
            account.last_four = zebra_form.cleaned_data['last_4_digits']
            account.stripe_customer_id = customer.id
            account.save()
            request.account = account
            request.account.update_account_status()

    else:
        zebra_form = StripePaymentForm()
    
    
    
    return locals()

@json_view
def save_account_info(request):
    success = False
    form = AccountForm(request.POST, instance=request.account)
    if form.is_valid():
        form.save()
        success = True

    return {"success":success}


def _my_forms(request):
    data = None
    if request.method == "POST":
        data = request.POST

    form = UserFormForUserAccount(data, instance=request.useraccount.user)
    useraccount_form = UserAccountNicknameForm(data, instance=request.useraccount)

    return form, useraccount_form

@render_to("accounts/manage_my_account.html")
def my_account(request):
    section = "admin"
    form, useraccount_form = _my_forms(request)
    return locals()

@json_view
def save_my_account_info(request):
    success = False
    form, useraccount_form = _my_forms(request)
    if form.is_valid() and useraccount_form.is_valid():
        form.save()
        useraccount_form.save()
        success = True
    

    return {"success":success}

@json_view
def change_my_password(request):
    success = False
    try:

        me = request.useraccount.user
        new_password = request.POST['new_password']
        me.set_password(new_password)
        me.save()
        success=True
    except:
        pass

    return {"success":success}

def reactivate_subscription(request):
    if not request.useraccount.is_admin:
        return HttpResponseRedirect(reverse("dashboard:dashboard"))

    request.account.chargify_subscription.reactivate()


    request.account.update_account_status()
    return HttpResponseRedirect(reverse("accounts:manage_account"))

@render_to("accounts/confirm_account_delete.html")
def confirm_account_delete(request):
    if not request.useraccount.is_admin:
        return HttpResponseRedirect(reverse("dashboard:dashboard"))
    
    return locals()


def do_account_delete(request):
    from accounts.models import Account

    if not request.useraccount.is_admin and not request.method == "POST":
        return HttpResponseRedirect(reverse("dashboard:dashboard"))
    
    account_id = request.POST['account_pk']
    assert int(account_id) == request.account.pk
    a = request.account
    a.delete()

    # print "all accounts"
    # print Account.objects.all()
    # print "deleted"

    return HttpResponseRedirect( "http://%s/account-deleted" % (settings.BASE_DOMAIN))
