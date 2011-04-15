from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from people.models import Person, Organization, PeopleAndOrganizationsSearchProxy, Employee
from people.forms import PersonForm, OrganizationForm, PersonViaOrganizationForm, EmployeeForm, EmployeeFormset, EmployeeFormsetFromOrg

from volunteers.views import _render_people_volunteer_tab 
from conversations.views import _render_people_conversations_tab
from donors.views import _render_people_donor_tab
from recent_activity.views import _render_people_recent_activity_tab 
from generic_tags.views import _render_people_tag_tab


@render_to("people/search.html")
def search(request):
    people_proxies = PeopleAndOrganizationsSearchProxy.objects(request).all()
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            people_proxies = PeopleAndOrganizationsSearchProxy.search(q,ignorable_chars=["-","(",")"])
    return locals()

@json_view
def search_results(request):
    people_proxies = PeopleAndOrganizationsSearchProxy.objects(request).all()
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            people_proxies = PeopleAndOrganizationsSearchProxy.search(q,ignorable_chars=["-","(",")"])

    return {"fragments":{"main_search_results":render_to_string("people/_search_results.html", locals())}}

def _basic_forms(person, request):
    data = None
    if request.method == "POST":
        data = request.POST


    form             = PersonForm(data, instance=person)
    employee_formset = EmployeeFormset(data, instance=person, prefix="ROLE")


    return (form, employee_formset)

@render_to("people/person.html")
def person(request, person_id):
    person = get_object_or_404(Person,pk=person_id)
    (form, employee_formset) = _basic_forms(person, request)
    return locals()

@json_view
def save_person_basic_info(request, person_id):
    person = get_object_or_404(Person,pk=person_id)
    (form, employee_formset) = _basic_forms(person, request)
    success = False
    if form.is_valid() and employee_formset.is_valid():
        person = form.save()
        employee_formset.save()
        success = True

    return {"success":success}


def new_person(request):
    person = Person.raw_objects.create(account=request.account)
    return HttpResponseRedirect("%s?edit=ON" %reverse("people:person",args=(person.pk,)))

def delete_person(request):
    try:
        if request.method == "POST":
            pk = request.POST['person_pk']
            person = Person.objects.get(pk=pk)
            person.delete()
    except:
        pass

    return HttpResponseRedirect(reverse("people:search"))


def _org_forms(org, request):
    data = None
    if request.method == "POST":
        data = request.POST
    
    form = OrganizationForm(data, instance=org)
    form_new_person = PersonViaOrganizationForm(data, prefix="NEWPERSON")
    form_employee = EmployeeForm(data, prefix="EMPLOYEE")

    try:
        employee_formset = EmployeeFormsetFromOrg(data, instance=org, prefix="ROLE")
    except:
        employee_formset = None
    
    return (form, form_new_person, form_employee, employee_formset)

def new_organization(request):
    org = Organization.raw_objects.create(account=request.account)
    return HttpResponseRedirect("%s?edit=ON" %reverse("people:organization",args=(org.pk,)))

def delete_organization(request):
    try:
        if request.method == "POST":
            pk = request.POST['org_pk']
            org = Organization.objects(request).get(pk=pk)
            org.delete()
    except:
        pass

    return HttpResponseRedirect(reverse("people:search"))


@render_to("people/organization.html")
def organization(request, org_id):
    org = get_object_or_404(Organization,pk=org_id)
    (form, form_new_person, form_employee, employee_formset) = _org_forms(org, request)
    if form.is_valid():
        form.save()

    return locals()

@json_view
def save_organization_basic_info(request,  org_id):
    org = get_object_or_404(Organization,pk=org_id)
    (form, form_new_person, form_employee, employee_formset) = _org_forms(org, request)
    success = False
    if form.is_valid():
        form.save()
        success = True

    return {"success":success}

def remove_employee(request, org_id, emp_id):
    org = get_object_or_404(Organization,pk=org_id)
    emp = get_object_or_404(Employee, pk=emp_id)
    try:
        assert emp.organization == org
        emp.delete()
        success = True
    except:
        success = False

    if request.is_ajax():
        return json_view({"success":success})
    else:
        return HttpResponseRedirect(reverse("people:organization",args=(org.pk,)))        

@json_view
def save_organization_employees(request,  org_id):
    org = get_object_or_404(Organization,pk=org_id)
    (form, form_new_person, form_employee, employee_formset) = _org_forms(org, request)
    success = False
    if employee_formset.is_valid():
        employee_formset.save()
        success = True

    return {"success":success}


def existing_person_via_organization(request, org_id):
    org = get_object_or_404(Organization,pk=org_id)
    try: 
        person_id = int(request.POST['person_pk'])
        person = Person.objects(request).get(pk=person_id)
        (form, form_new_person, form_employee, employee_formset) = _org_forms(org, request)
        if form_employee.is_valid():
            employee = form_employee.save(commit=False)
            employee.person = person
            employee.organization = org
            employee.save()
    except:
        pass
    return HttpResponseRedirect(reverse("people:organization",args=(org.pk,)))


def new_person_via_organization(request, org_id):
    org = get_object_or_404(Organization,pk=org_id)
    (form, form_new_person, form_employee, employee_formset) = _org_forms(org, request)
    if form_new_person.is_valid():
        person = form_new_person.save()
        success = True
    
    if form_employee.is_valid():
        employee = form_employee.save(commit=False)
        employee.person = person
        employee.organization = org
        employee.save()

    return HttpResponseRedirect(reverse("people:organization",args=(org.pk,)))

@json_view
def add_person_via_organization_search_results(request):
    people = Person.objects(request).none()
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            people = Person.search(q,ignorable_chars=["-","(",")"])

    return {"fragments":{"new_person_search_results":render_to_string("people/_add_person_to_org_results.html", locals())}}


@json_view
def tab_contents(request, person_id, tab_name=None):
    success = False
    person = Person.objects(request).get(pk=person_id)
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