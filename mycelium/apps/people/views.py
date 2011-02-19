from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from people.models import Person, Organization, PeopleAndOrganizationsSearchProxy
from people.forms import PersonForm, EmailForm, AddressForm, PhoneForm, OrganizationForm, PersonViaOrganizationForm, EmployeeForm

@render_to("people/search.html")
def search(request):
    people_proxies = PeopleAndOrganizationsSearchProxy.objects.all()
    return locals()

@json_view
def search_results(request):
    people_proxies = PeopleAndOrganizationsSearchProxy.objects.all()
    if 'q' in request.GET:
        q = request.GET['q']
        print q
        if q != "":
            people_proxies = PeopleAndOrganizationsSearchProxy.search(q,ignorable_chars=["-","(",")"])

    return {"fragments":{"main_search_results":render_to_string("people/_search_results.html", locals())}}

def _basic_forms(person, request):
    data = None
    if request.method == "POST":
        data = request.POST

    form         = PersonForm(data, instance=person)
    email_form   = EmailForm(data, instance=person.primary_email)
    address_form = AddressForm(data, instance=person.primary_address)
    phone_form   = PhoneForm(data, instance=person.primary_phone_number)

    return (form, email_form, address_form, phone_form)

@render_to("people/person.html")
def person(request, person_id):
    person = get_object_or_404(Person,pk=person_id)
    form, email_form, address_form, phone_form = _basic_forms(person, request)
    return locals()

@json_view
def save_person_basic_info(request, person_id):
    person = get_object_or_404(Person,pk=person_id)
    form, email_form, address_form, phone_form = _basic_forms(person, request)
    success = False
    if form.is_valid():
        person = form.save()
        
        if email_form.is_valid():
            email = email_form.save(commit=False)
            email.person = person
            email.save()

        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.person = person
            address.save()

        if phone_form.is_valid():
            phone = phone_form.save(commit=False)
            phone.person = person
            phone.save()
            
        success = True
    else:
        print "invalid"
        # print form
        # print email_form
        # print address_form
        # print phone_form
    return {"success":success}


def new_person(request):
    person = Person.objects.create()
    return HttpResponseRedirect("%s?edit=ON" %reverse("people:person",args=(person.pk,)))


def _org_forms(org, request):
    data = None
    if request.method == "POST":
        data = request.POST
    
    form = OrganizationForm(data, instance=org)
    form_new_person = PersonViaOrganizationForm(data, prefix="NEWPERSON")
    form_employee = EmployeeForm(data, prefix="EMPLOYEE")
    
    return (form, form_new_person, form_employee)

def new_organization(request):
    org = Organization.objects.create()
    return HttpResponseRedirect("%s?edit=ON" %reverse("people:organization",args=(org.pk,)))

@render_to("people/organization.html")
def organization(request, org_id):
    org = get_object_or_404(Organization,pk=org_id)
    (form, form_new_person, form_employee) = _org_forms(org, request)
    if form.is_valid():
        form.save()

    return locals()

@json_view
def save_organization_basic_info(request,  org_id):
    org = get_object_or_404(Organization,pk=org_id)
    (form, form_new_person, form_employee) = _org_forms(org, request)
    success = False
    if form.is_valid():
        form.save()
        success = True

    return {"success":success}

def existing_person_via_organization(request, org_id):
    org = get_object_or_404(Organization,pk=org_id)
    try: 
        person_id = int(request.POST['person_pk'])
        person = Person.objects.get(pk=person_id)
        (form, form_new_person, form_employee) = _org_forms(org, request)
        if form_employee.is_valid():
            employee = form_employee.save(commit=False)
            employee.person = person
            employee.organization = org
            employee.save()
    except:
        pass
    return HttpResponseRedirect("%s" %reverse("people:organization",args=(org.pk,)))


def new_person_via_organization(request, org_id):
    org = get_object_or_404(Organization,pk=org_id)
    (form, form_new_person, form_employee) = _org_forms(org, request)
    if form_new_person.is_valid():
        person = form_new_person.save()
        success = True
    
    if form_employee.is_valid():
        employee = form_employee.save(commit=False)
        employee.person = person
        employee.organization = org
        employee.save()

    return HttpResponseRedirect("%s" %reverse("people:organization",args=(org.pk,)))

@json_view
def add_person_via_organization_search_results(request):
    people = Person.objects.none()
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            people = Person.search(q,ignorable_chars=["-","(",")"])

    return {"fragments":{"new_person_search_results":render_to_string("people/_add_person_to_org_results.html", locals())}}
