from django.template import RequestContext
from django.conf import settings
from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page
from django.core.validators import validate_email

# import mailchimp
from email_list.models import EmailSubscription
from marketing_site.forms import EmailForm


@render_to("hi/hi.html")
def hi(request):
    form = EmailForm()
    save_success=False
    
    if request.method == "POST":
        posted = True

        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            save_success=True

    return locals()
