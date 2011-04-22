from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page


from people.models import Person
from volunteers.models import Volunteer, CompletedShift
from volunteers.forms import NewShiftForm, VolunteerStatusForm

VOLUNTEER_STATUS_PREFIX = "VOLUNTEER_STATUS"

def _render_people_volunteer_tab(context):

    form = NewShiftForm(account=context["request"].account)
    status_form = VolunteerStatusForm(prefix=VOLUNTEER_STATUS_PREFIX, instance=context["person"].volunteer, account=context["request"].account)
    context.update({"form":form,"status_form":status_form,})
    return render_to_string("volunteers/_people_volunteer_tab.html", RequestContext(context["request"],context))
    

def _return_fragments_or_redirect(request,context):
    if request.is_ajax():
        return HttpResponse(simplejson.dumps( {"fragments":{"detail_tab":_render_people_volunteer_tab(context)}}))
    else:
        return HttpResponseRedirect(reverse("people:person",args=(context["person"].pk,)))    


def save_completed_volunteer_shift(request, volunteer_id):
    volunteer = get_or_404_by_account(Volunteer, request.account, volunteer_id)
    person = volunteer.person
    if request.method == "POST":
        form = NewShiftForm(request.POST, account=request.account)
        if form.is_valid():
            completed_shift = form.save(commit=False)
            completed_shift.volunteer = volunteer
            completed_shift.save()
    obj = volunteer
    return _return_fragments_or_redirect(request,locals())
    


def delete_completed_volunteer_from_people_tab(request, volunteer_shift_id):

    cs = get_or_404_by_account(CompletedShift, request.account, volunteer_shift_id)
    volunteer = cs.volunteer
    person = volunteer.person
    cs.delete()
    obj = volunteer
    return _return_fragments_or_redirect(request,locals())
    
def save_status(request, volunteer_id):
    volunteer = get_or_404_by_account(Volunteer, request.account, volunteer_id)
    person = volunteer.person
    if request.method == "POST":
        status_form = VolunteerStatusForm(request.POST, prefix=VOLUNTEER_STATUS_PREFIX, instance=volunteer, account=request.account)
        if status_form.is_valid():
            status_form.save()

    return _return_fragments_or_redirect(request,locals())

