from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from people.models import Person
from people.forms import PersonForm, EmailForm, AddressForm, PhoneForm

@render_to("people/search.html")
def search(request):
    people = Person.objects.all()
    return locals()

@json_view
def search_results(request):
    if 'q' in request.GET:
        q = request.GET['q']
        people = Person.search(q,ignorable_chars=["-","(",")"])
    else:
        people = Person.objects.all()
    return {"html":render_to_string("people/_search_results.html", locals())}

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
        print form
        print email_form
        print address_form
        print phone_form
    return {"success":success}


def new_person(request):
    person = Person.objects.create()
    return HttpResponseRedirect("%s?edit=ON" %reverse("people:person",args=(person.pk,)))
