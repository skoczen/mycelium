import time 
from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *

from people.models import Person, PeopleSearchProxy, PersonPhoneNumber, PersonEmailAddress
from people.forms import PersonForm, PhoneNumberFormset, EmailAddressFormset, PhoneNumberForm, EmailAddressForm
from organizations.models import Employee
from organizations.forms import OrganizationForm, PersonViaOrganizationForm, EmployeeForm, EmployeeFormset, EmployeeFormsetFromOrg

from conversations.views import _render_people_conversations_tab, _people_conversations_tab_context
from volunteers.views import _render_people_volunteer_tab
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


def _person_form(person, request, data):
    return PersonForm(data, instance=person, account=request.account)

def _employee_form(person, request, data):
    return EmployeeForm(data, instance=person, prefix="ROLE", account=request.account)

def _phone_number_form(phone_number, request, data):
    return PhoneNumberForm(data, instance=phone_number, prefix="PHONE", account=request.account)

def _email_form(email, request, data):
    return EmailAddressForm(data, instance=email, prefix="EMAIL", account=request.account)

def _employee_formset(employee, request, data):
    return EmployeeFormset(data, instance=employee, prefix="ROLE", account=request.account)

def _phone_number_formset(person, request, data):
    return PhoneNumberFormset(data, instance=person, prefix="PHONE", account=request.account)

def _email_formset(person, request, data):
    return EmailAddressFormset(data, instance=person, prefix="EMAIL", account=request.account)

def _basic_forms(person, request):
    data = None
    if request.method == "POST":
        data = request.POST

    form             = _person_form(person, request, data)
    employee_formset = _employee_formset(person, request, data)
    phone_formset    = _phone_number_formset(person, request, data)
    email_formset    = _email_formset(person, request, data)

    return (form, employee_formset, phone_formset, email_formset)


@render_to("people/person.html")
def person(request, person_id):
    person = get_or_404_by_account(Person, request.account, person_id)
    (form, employee_formset, phone_formset, email_formset) = _basic_forms(person, request)
    c = locals()
    return _people_conversations_tab_context(c)

@json_view
def save_person_basic_info(request, person_id):
    person = get_or_404_by_account(Person, request.account, person_id)
    (form, employee_formset, phone_formset, email_formset) = _basic_forms(person, request)
    success = False
    if form.is_valid() and employee_formset.is_valid() and phone_formset.is_valid() and email_formset.is_valid():
        person = form.save(commit=False)
        employee_formset.save()
        phone_formset.save()
        email_formset.save()
        person.save()
        success = True
        save_action.delay(request.account, request.useraccount, "updated a person", person=person,)
    else:
        print form, employee_formset, phone_formset, email_formset

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


#  Generic Form Handling

def _get_generic_ajax_data(post_data):

    page_pk = post_data.get("page_pk", None)
    db_pk = post_data.get("db_pk", None)
    form_object_type = post_data.get("form_object_type", None)
    data = post_data
    if not page_pk or not data or not form_object_type:
        raise Exception, "Missing post data"

    time.sleep(2)
    return page_pk, db_pk, data, form_object_type

def _generic_ajax_response(d):
    return {
        "form_object_type": d["form_object_type"],
        "page_pk":d["page_pk"],
        "db_pk":d["db_pk"],
        "event_success":d["success"],
        "error_string":getattr(d,"success",False)
    }

@json_view
def person_save(request):
    success = False
    page_pk, db_pk, data, form_object_type = _get_generic_ajax_data(request.POST)
    person = get_or_404_by_account(Person, request.account, db_pk)

    time.sleep(1)
    form = _person_form(person, request, data)
    if form.is_valid():
        form.save()
        success = True
        save_action.delay(request.account, request.useraccount, "updated a person", person=person,)

    return _generic_ajax_response(locals())


@json_view
def person_new(request):
    success = False
    page_pk, db_pk, data, form_object_type = _get_generic_ajax_data(request.POST)
    raise Exception, "Not Implemented"

    success = True
    return _generic_ajax_response(locals())

@json_view
def person_delete(request):
    success = False
    page_pk, db_pk, data, form_object_type = _get_generic_ajax_data(request.POST)
    person = get_or_404_by_account(Person, request.account, db_pk)
    person.delete()
    db_pk = None

    success = True
    return _generic_ajax_response(locals())


def _person_related_model_save(cls, request, form_builder):
    success = False
    page_pk, db_pk, data, form_object_type = _get_generic_ajax_data(request.POST)
    person = get_or_404_by_account(Person, request.account, request.POST["person_pk"])
    obj = get_or_404_by_account(cls, request.account, db_pk)
    form = form_builder(obj, request, data)
    if form.is_valid():
        form.save()
        success = True
        save_action.delay(request.account, request.useraccount, "updated a person", person=person,) 
    else:
        error_string = form.errors
    return _generic_ajax_response(locals())

def _person_related_model_new(cls, request, form_builder):
    success = False
    page_pk, db_pk, data, form_object_type = _get_generic_ajax_data(request.POST)
    person = get_or_404_by_account(Person, request.account, request.POST["person_pk"])
    obj = cls.raw_objects.create(account=request.account)
    form = form_builder(obj, data, request)
    if form.is_valid():
        form.save()
        success = True
        save_action.delay(request.account, request.useraccount, "updated a person", person=person,)    
        db_pk = phone_number.pk
    else:
        error_string = form.errors

    return _generic_ajax_response(locals())

def _person_related_model_delete(cls, request):
    success = False
    page_pk, db_pk, data, form_object_type = _get_generic_ajax_data(request.POST)
    obj = get_or_404_by_account(cls, request.account, db_pk)
    obj.delete()
    db_pk = None
    save_action.delay(request.account, request.useraccount, "updated a person", person=person,)    

    success = True
    return _generic_ajax_response(locals())


@json_view
def phone_number_save(request):
    return _person_related_model_save(PersonPhoneNumber, request, _phone_number_form)

@json_view
def phone_number_new(request):
    return _person_related_model_new(PersonPhoneNumber, request, _phone_number_form)

@json_view
def phone_number_delete(request):
    return _person_related_model_delete(PersonPhoneNumber, request)


@json_view
def email_save(request):
    return _person_related_model_save(PersonEmailAddress, request, _email_form)

@json_view
def email_new(request):
    return _person_related_model_new(PersonEmailAddress, request, _email_form)

@json_view
def email_delete(request):
    return _person_related_model_delete(PersonEmailAddress, request)


@json_view
def employee_save(request):
    return _person_related_model_save(Employee, request, _employee_form)

@json_view
def employee_new(request):
    return _person_related_model_new(Employee, request, _employee_form)

@json_view
def employee_delete(request):
    return _person_related_model_delete(Employee, request)
