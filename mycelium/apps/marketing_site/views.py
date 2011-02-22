from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
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
from marketing_site.models import GoodCloudEmployee

@render_to("marketing_site/home.html")
def home(request):
    form = EmailForm()
    save_success=False
    
    if request.method == "POST":
        posted = True

        form = EmailForm(request.POST)
        if form.is_valid():
            form.save()
            try:
                from django.core.mail import send_mail
                for email in settings.MANAGERS:
                    send_mail("New Email Signup!", "%s" % render_to_string("marketing_site/new_signup_email.txt", form.cleaned_data), settings.SERVER_EMAIL, [email[1]])
            except:
                from qi_toolkit.helpers import print_exception
                print_exception()
                pass
            save_success=True

    return locals()


@render_to("marketing_site/about_us.html")
def about_us(request):
    all_employees = GoodCloudEmployee.objects.all()
    return locals()