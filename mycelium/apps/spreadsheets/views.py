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
from spreadsheets.models import Spreadsheet, SpreadsheetSearchProxy
from spreadsheets.forms import SpreadsheetForm
from johnny import cache as jcache

def _basic_forms(spreadsheet, request, no_data=False):
    data = None
    if not no_data and request and request.method == "POST":
        data = request.POST
    
    account = request.account
    spreadsheet_form = SpreadsheetForm(data, instance=spreadsheet, account=account)
    
    return spreadsheet_form



@render_to("spreadsheets/search.html")
def search(request):
    section = "spreadsheets"
    search_proxies = SpreadsheetSearchProxy.objects_by_account(request.account).all()
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            search_proxies = SpreadsheetSearchProxy.search(request.account, q,ignorable_chars=["-","(",")"])
    return locals()

@json_view
def search_results(request):
    section = "spreadsheets"
    search_proxies = SpreadsheetSearchProxy.objects_by_account(request.account).all()
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            search_proxies = SpreadsheetSearchProxy.search(request.account, q,ignorable_chars=["-","(",")"])

    return {"fragments":{"main_search_results":render_to_string("spreadsheets/_search_results.html", locals())}}


@render_to("spreadsheets/spreadsheet.html")
def spreadsheet(request, spreadsheet_id):
    spreadsheet = get_or_404_by_account(Spreadsheet, request.account, spreadsheet_id)
    form = _basic_forms(spreadsheet, request, no_data=True)
    if spreadsheet_id == "new":
        new_spreadsheet == True
    section = "spreadsheets"
    return locals()


@json_view
def save_basic_info(request, spreadsheet_id):
    spreadsheet = get_or_404_by_account(Spreadsheet, request.account, spreadsheet_id, using='default')
    form = _basic_forms(spreadsheet, request)
    success = False

    if form.is_valid():
        spreadsheet = form.save()
        jcache.invalidate(SpreadsheetSearchProxy)
        success = True

    # form = _basic_forms(spreadsheet, request, no_data=True)

    return {"success":success}



# @render_to("spreadsheets/detail_volunteer.html")
def download(request, type, spreadsheet_id):
    spreadsheet = get_or_404_by_account(Spreadsheet, request.account, spreadsheet_id)
    if spreadsheet_id == "new":
        new_spreadsheet == True
    section = "spreadsheets"
    return locals()

    
@render_to("spreadsheets/new.html")
def new(request):
    spreadsheet = Spreadsheet.raw_objects.using('default').create(account=request.account)
    return HttpResponseRedirect("%s?edit=ON" %reverse("spreadsheets:spreadsheet",args=(spreadsheet.pk,)))

    

def delete(request):
    try:
        if request.method == "POST":
            pk = request.POST['spreadsheet_pk']
            spreadsheet = get_or_404_by_account(Spreadsheet, request.account, pk, using='default')
            spreadsheet.delete()
    except:
        pass

    return HttpResponseRedirect(reverse("spreadsheets:search"))
