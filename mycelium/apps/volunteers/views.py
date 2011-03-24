from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
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
from generic_tags.views import TagViews

VOLUNTEER_STATUS_PREFIX = "VOLUNTEER_STATUS"

def _render_people_volunteer_tab(context):
    form = NewShiftForm()
    status_form = VolunteerStatusForm(prefix=VOLUNTEER_STATUS_PREFIX, instance=context["person"].volunteer)
    all_skills = Volunteer.skills.all()
    tag_view_obj = skill_views 
    context.update({"form":form,"status_form":status_form,"all_skills":all_skills,'tag_view_obj':tag_view_obj})
    return render_to_string("volunteers/_people_volunteer_tab.html", RequestContext(context["request"],context))
    

def _return_fragments_or_redirect(request,context):
    if request.is_ajax():
        return HttpResponse(simplejson.dumps( {"fragments":{"detail_tab":_render_people_volunteer_tab(context)}}))
    else:
        return HttpResponseRedirect(reverse("people:person",args=(context["person"].pk,)))    


def save_completed_volunteer_shift(request, volunteer_id):
    volunteer = Volunteer.objects.get(pk=int(volunteer_id))
    person = volunteer.person
    if request.method == "POST":
        form = NewShiftForm(request.POST)
        if form.is_valid():
            completed_shift = form.save(commit=False)
            completed_shift.volunteer = volunteer
            completed_shift.save()
    obj = volunteer
    return _return_fragments_or_redirect(request,locals())
    


def delete_completed_volunteer_from_people_tab(request, volunteer_shift_id):
    cs = CompletedShift.objects.get(pk=volunteer_shift_id)
    volunteer = cs.volunteer
    person = volunteer.person
    cs.delete()
    obj = volunteer
    return _return_fragments_or_redirect(request,locals())
    
def save_status(request, volunteer_id):
    volunteer = Volunteer.objects.get(pk=int(volunteer_id))
    person = volunteer.person
    if request.method == "POST":
        status_form = VolunteerStatusForm(request.POST, prefix=VOLUNTEER_STATUS_PREFIX, instance=volunteer)
        if status_form.is_valid():
            status_form.save()

    return _return_fragments_or_redirect(request,locals())


class VolunteerTagViews(TagViews):
    TargetModel = Volunteer
    namespace_name = "volunteer"
    default_redirect_url = "people:person"
    app_name = "volunteers"
    tag_field = "skills"
    mode = "checklist"
    new_tag_placeholder = "New skill/role"
    def _default_redirect_args(self, context):
        return (context["obj"].person.pk,)

skill_views = VolunteerTagViews()
