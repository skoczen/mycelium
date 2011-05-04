from django.forms import ModelForm, ModelChoiceField, CharField, Form
from django.forms.widgets import RadioSelect, PasswordInput
from django.forms.models import BaseModelFormSet, BaseInlineFormSet, inlineformset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from accounts.models import Account, Plan, AccessLevel, UserAccount

def adjust_queryset_for_account_based_models(f, *args, **kwargs):
    if hasattr(f,"queryset"):
        print "has queryset"
    
def _get_account_from_kwargs(kwargs):
    account = None
    if "account" in kwargs:
        account = kwargs["account"]
        # print "from account"
    elif "request" in kwargs and kwargs["request"].account:
        account = kwargs["request"].account
        # print "from request"
    if not account:
        if "instance" in kwargs and kwargs["instance"] and hasattr(kwargs["instance"],"account"):
            account = kwargs["instance"].account
            # print "pulled from instance: %s" % kwargs["instance"]
    assert account, "Account required"
    # print "found account: %s" % account
            
    return account

class AccountBasedModelForm(ModelForm):
    account = ModelChoiceField(queryset=Account.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        if not hasattr(self,"account"):
            self.account = _get_account_from_kwargs(kwargs)
        
        account = _get_account_from_kwargs(kwargs)
        if "account" in kwargs:
            del kwargs["account"]
        if "request" in kwargs:
            del kwargs["request"]    

        
        super(AccountBasedModelForm, self).__init__(*args,**kwargs)
        
        
        for k,v in self.fields.iteritems():
            if hasattr(v,"queryset") and k != "account":
                v.queryset = v.queryset.filter(account=account)
        self.fields["account"].queryset = Account.objects.filter(pk=account.pk)
        

    def clean(self):
        if hasattr(self, "cleaned_data"):
            cleaned_data = self.cleaned_data
            cleaned_data["account"] = self.account
            return cleaned_data
    
class AccountBasedModelFormSet(BaseInlineFormSet):
    account = ModelChoiceField(queryset=Account.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        if not hasattr(self,"account"):
            self.account = _get_account_from_kwargs(kwargs)

        account = _get_account_from_kwargs(kwargs)
        if "account" in kwargs:
            del kwargs["account"]
        if "request" in kwargs:
            del kwargs["request"]

        super(AccountBasedModelFormSet, self).__init__(*args,**kwargs)
        
        for f in self.forms:
            f.fields["account"].queryset = Account.objects.filter(pk=account.pk)
        

    def clean(self):
        super(AccountBasedModelFormSet, self).clean()
        for f in self.forms:
            if hasattr(f, "cleaned_data"):
                f.cleaned_data["account"] = self.account
        

class AccountAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, auth_request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.auth_request = auth_request
        self.user_cache = None
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        self.auth_request = auth_request

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(auth_request=self.auth_request, username=username, password=password)
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


class NewAccountForm(ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data["plan"] = Plan.monthly_plan()
        
        return cleaned_data

    class Meta:
        model = Account
        fields = ("name", "subdomain", "plan", "agreed_to_terms")

class AccountForm(ModelForm):
    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data["plan"] = Plan.monthly_plan()
        
        return cleaned_data

    class Meta:
        model = Account
        fields = ("name", "plan")


class NewUserForm( Form):
    username    = CharField(max_length=100, required=True)
    email       = CharField(max_length=255, required=True)
    password    = CharField(max_length=255, required=True)
    first_name  = CharField(max_length=255, required=True)


class UserAccountAccessForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserAccountAccessForm, self).__init__(*args, **kwargs)
        # Really, django?  This is necessary for a Non-null field??
        self.fields["access_level"].choices = [c for c in self.fields["access_level"].choices][1:]


    class Meta:
        model = UserAccount
        fields = ("access_level",)
        widgets = {
            'access_level': RadioSelect
        }


class UserFormForUserAccount(ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserFormForUserAccount, self).__init__(*args, **kwargs)
        self.initial["username"] = self.instance.get_profile().denamespaced_username

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data["username"] = self.instance.get_profile().account.namespaced_username_for_username(cleaned_data["username"])
       
        return cleaned_data


    class Meta:
        model = User
        fields = ("first_name", "username", "email",)

class NewUserAccountForm(UserAccountAccessForm):
    username    = CharField(max_length=100, required=True)
    email       = CharField(max_length=255, required=True)
    password    = CharField(max_length=255, required=True, widget=PasswordInput)
    first_name  = CharField(max_length=255, required=True, label="Full Name")


class UserAccountAccessFormsetBase(AccountBasedModelFormSet):
    pass

UserAccountAccessFormset = inlineformset_factory(Account, UserAccount, fields=("access_level",), can_delete=False, extra=0, form=UserAccountAccessForm,  )