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

@csrf_protect
@never_cache
def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm):
    """Displays the login form and handles the login action."""

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST, auth_request=request)
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

            return HttpResponseRedirect(redirect_to)

    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    return render_to_response(template_name, {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))


from qi_toolkit.helpers import *
from accounts.forms import UserAccountAccessFormset, NewUserAccountForm
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from accounts.models import UserAccount
def _account_forms(request):
    data = None
    if request.method == "POST":
        data = request.POST

    user_access_formset = UserAccountAccessFormset(data,instance=request.account)
    new_user_form = NewUserAccountForm(data)
    return user_access_formset, new_user_form

@render_to("accounts/manage_users.html")
def manage_users(request):
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

    ua = get_object_or_404(UserAccount,account=request.account, pk=ua_id)
    user = ua.user
    user.set_password("changeme!")
    user.save()

    return {"success":success}

def delete_account(request, ua_id):
    ua = get_object_or_404(UserAccount,account=request.account, pk=ua_id)
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


