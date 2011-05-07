from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response
from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from people.models import Person
import random

@render_to("reports/search.html")
def search(request):
    # TODO: this is obnoxious.  Fix it.
    section = "reports"
    return locals()

@render_to("reports/detail_volunteer.html")
def detail(request, report_id):
    # report = get_or_404_by_account(Report, request.account, report_id)
    if report_id == "new":
        new_report == True
    section = "reports"
    people = Person.objects_by_account(request.account).order_by("?").all()
    hours = [random.randint(2,280) for i in range(0,50)]
    return locals()

# TODO: clear this out
def report_demo_page(request):
    section = "reports"
    people = Person.objects_by_account(request.account).order_by("?").all()
    hours = [random.randint(2,280) for i in range(0,50)]
    return locals()
    

@render_to("reports/detail_volunteer.html")
def detail_volunteer(request):
    return report_demo_page(request)

@render_to("reports/detail_donors.html")
def detail_donors(request):
    return report_demo_page(request)
    
@render_to("reports/detail_email.html")
def detail_email(request):
    return report_demo_page(request)

    
@render_to("reports/new.html")
def new(request, report_id):
    # Eventually, this should go away. It's just for test.
    section = "reports"
    people = Person.objects_by_account(request.account).order_by("?").all()
    hours = [random.randint(2,280) for i in range(0,50)]
    return locals()