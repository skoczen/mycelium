from django.forms import ModelForm, ModelChoiceField
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django import forms
from django.utils.translation import ugettext_lazy as _
from accounts.models import Account

def adjust_queryset_for_account_based_models(f, *args, **kwargs):
    if hasattr(f,"queryset"):
        print "has queryset"
    


class AccountBasedModelForm(ModelForm):
    account = ModelChoiceField(queryset=Account.objects.all(), required=False)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(ModelForm, self).__init__(*args,**kwargs)
        self.fields["account"].queryset = Account.objects.filter(pk=self.request.account.pk)

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data["account"] = self.request.account
        return cleaned_data
    

class AccountAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(request=self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))
            elif not self.user_cache.is_active:
                raise forms.ValidationError(_("This account is inactive."))

        # TODO: determine whether this should move to its own method.
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_("Your Web browser doesn't appear to have cookies enabled. Cookies are required for logging in."))

        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache