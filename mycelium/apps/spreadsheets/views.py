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

@render_to("spreadsheets/search.html")
def search(request):
    # TODO: this is obnoxious.  Fix it.
    section = "spreadsheets"
    return locals()

@render_to("spreadsheets/detail_volunteer.html")
def detail(request, spreadsheet_id):
    # spreadsheet = get_or_404_by_account(Report, request.account, spreadsheet_id)
    if spreadsheet_id == "new":
        new_spreadsheet == True
    section = "spreadsheets"
    people = Person.objects_by_account(request.account).order_by("?").all()
    hours = [random.randint(2,280) for i in range(0,50)]
    return locals()

# TODO: clear this out
def spreadsheet_demo_page(request):
    section = "spreadsheets"
    people = Person.objects_by_account(request.account).order_by("?").all()
    hours = [random.randint(2,280) for i in range(0,50)]
    return locals()
    

@render_to("spreadsheets/detail_volunteer.html")
def detail_volunteer(request):
    return spreadsheet_demo_page(request)

@render_to("spreadsheets/detail_donors.html")
def detail_donors(request):
    return spreadsheet_demo_page(request)
    
@render_to("spreadsheets/detail_email.html")
def detail_email(request):
    return spreadsheet_demo_page(request)

    
@render_to("spreadsheets/new.html")
def new(request, spreadsheet_id):
    # Eventually, this should go away. It's just for test.
    section = "spreadsheets"
    people = Person.objects_by_account(request.account).order_by("?").all()
    hours = [random.randint(2,280) for i in range(0,50)]
    return locals()