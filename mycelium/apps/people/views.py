from django.template import RequestContext
from django.shortcuts import render_to_response
from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from people.models import Person, PeopleSearchProxy
from people.forms import PersonForm
from organizations.models import Employee
from organizations.forms import OrganizationForm, PersonViaOrganizationForm, EmployeeForm, EmployeeFormset, EmployeeFormsetFromOrg

from volunteers.views import _render_people_volunteer_tab, _people_volunteer_tab_context
from conversations.views import _render_people_conversations_tab, _people_conversations_tab_context
from donors.views import _render_people_donor_tab
from recent_activity.views import _render_people_recent_activity_tab 
from generic_tags.views import _render_people_tag_tab
from activities.tasks import save_action

@render_to("people/search.html")
def search(request):
    search_proxies = PeopleSearchProxy.objects_by_account(request.account).all()
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            search_proxies = PeopleSearchProxy.search(request.account, q,ignorable_chars=["-","(",")"])
    return locals()

@json_view
def search_results(request):
    search_proxies = PeopleSearchProxy.objects_by_account(request.account).all()
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            search_proxies = PeopleSearchProxy.search(request.account, q,ignorable_chars=["-","(",")"])

    return {"fragments":{"main_search_results":render_to_string("people/_search_results.html", locals())}}

def _basic_forms(person, request):
    data = None
    if request.method == "POST":
        data = request.POST


    form             = PersonForm(data, instance=person, account=request.account)
    employee_formset = EmployeeFormset(data, instance=person, prefix="ROLE", account=request.account)


    return (form, employee_formset)

@render_to("people/person.html")
def person(request, person_id):
    person = get_or_404_by_account(Person, request.account, person_id)
    (form, employee_formset) = _basic_forms(person, request)
    c = locals()
    return _people_conversations_tab_context(c)

@json_view
def save_person_basic_info(request, person_id):
    person = get_or_404_by_account(Person, request.account, person_id)
    (form, employee_formset) = _basic_forms(person, request)
    success = False
    if form.is_valid() and employee_formset.is_valid():
        person = form.save()
        employee_formset.save()
        success = True
        save_action.delay(request.account, request.useraccount, "updated a person", person=person,)

    return {"success":success}


def new_person(request):
    person = Person.raw_objects.create(account=request.account)
    save_action.delay(request.account, request.useraccount, "created a person", person=person,)
    return HttpResponseRedirect("%s?edit=ON" %reverse("people:person",args=(person.pk,)))

def delete_person(request):
    try:
        if request.method == "POST":
            pk = request.POST['person_pk']
            person = get_or_404_by_account(Person, request.account, pk)
            person.delete()
    except:
        pass

    return HttpResponseRedirect(reverse("people:search"))

@json_view
def tab_contents(request, person_id, tab_name=None):
    success = False
    person = get_or_404_by_account(Person, request.account, person_id)
    html = None
    if not tab_name and 'tab_name' in request.POST:
        tab_name = request.POST['tab_name'].strip()[1:]
    if request.method == "POST":
        if tab_name == "conversations":
            html = _render_people_conversations_tab(locals())
        elif tab_name == "recent_activity":
            html = _render_people_recent_activity_tab(locals())
        elif tab_name == "tags":
            html = _render_people_tag_tab(locals())    
        elif tab_name == "volunteer":
            html = _render_people_volunteer_tab(locals())
        elif tab_name == "donor":
            html = _render_people_donor_tab(locals())
    if html:
        return {"fragments":{"detail_tab":html}}  
    else:
        return {}