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

from email_list.models import EmailSubscription
from email_list import GOODCLOUD_TIMES_KEY
from marketing_site.forms import EmailForm
from marketing_site.models import GoodCloudEmployee

@render_to("marketing_site/home.html")
def home(request):
    return locals()

    
@render_to("marketing_site/ssl_page.html")
def ssl_page(request):
    return locals()


@render_to("marketing_site/about_us.html")
def about_us(request):
    all_employees = GoodCloudEmployee.objects.all()
    return locals()

@render_to("marketing_site/features.html")
def features(request):
    return locals()

@render_to("marketing_site/tour.html")
def tour(request):
    return locals()

@render_to("marketing_site/screenshots.html")
def screenshots(request):
    return locals()

@render_to("marketing_site/newsletter.html")
def newsletter(request):
    form = EmailForm()
    save_success=False
    newsletter_subscriber = request.session.get('newsletter_subscriber', False)
    save_success = request.GET.get('save_success', None)

    if request.method == "POST":
        posted = True

        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            form.save()
            request.session['newsletter_subscriber'] = email
            save_success=True
            # Set a cookie, so we remember them.
            return HttpResponseRedirect("%s?save_success=True" %reverse("marketing_site:newsletter"))
            
    return locals()

@render_to("marketing_site/praise.html")
def praise(request):
    return locals()

@render_to("marketing_site/pricing.html")
def pricing(request):
    return locals()


@render_to("marketing_site/legal.html")
def legal(request):
    return locals()

@render_to("marketing_site/contact_us.html")
def contact_us(request):
    return locals()


def newsletter_issue(request, year, month):
    form = EmailForm()
    save_success=False
    newsletter_subscriber = request.session.get('newsletter_subscriber', False)
    save_success = request.GET.get('save_success', None)

    if request.method == "POST":
        posted = True

        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            form.save()
            request.session['newsletter_subscriber'] = email
            save_success=True
            # Set a cookie, so we remember them.
            return HttpResponseRedirect("%s?save_success=True" %reverse("marketing_site:newsletter_issue", args=(year, month)))
            
    return render_to_response("marketing_site/newsletter/%s_%02d.html" % (year, int(month),), RequestContext(request, locals()))

