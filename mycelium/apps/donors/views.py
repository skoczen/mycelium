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

from donors.forms import NewDonationForm
from donors.models import Donor

def _render_people_donor_tab(context):
    donation_form = NewDonationForm()
    context.update({"donation_form":donation_form,"donor":context["person"].donor})
    return render_to_string("donors/_people_donor_tab.html", RequestContext(context["request"],context))

def _return_fragments_or_redirect(request,context):
    if request.is_ajax():
        return HttpResponse(simplejson.dumps( {"fragments":{"detail_tab":_render_people_donor_tab(context)}}))
    else:
        return HttpResponseRedirect(reverse("people:person",args=(person.pk,)))    


def save_new_donation(request, donor_id):
    donor = Donor.objects.get(pk=int(donor_id))
    person = donor.person
    if request.method == "POST":
        form = NewDonationForm(request.POST)
        if form.is_valid():
            new_donation = form.save(commit=False)
            new_donation.donor = donor
            new_donation.save()

    return _return_fragments_or_redirect(request,locals())
    

def delete_donation_from_people_tab(request, donation_id):
    d = Donation.objects.get(pk=donation_id)
    donor = d.donor
    person = donor.person
    d.delete()

    return _return_fragments_or_redirect(request,locals())
    



def _update_with_tag_fragments(context):
    d = {
        "fragments":{'donor_tags': render_to_string("donors/_donor_tags.html", RequestContext(context["request"],context)),},
        "success": context["success"],
    }
    return d

def add_donor_tag(request):
    success = False
    if request.method == "POST":
        pk = int(request.POST['donor_pk'])
        new_tag = request.POST['new_tag'].strip().lower()
        if new_tag != "":
            donor = Donor.objects.get(pk=pk)
            donor.tags.add(new_tag)
            success = True

    if request.is_ajax():
        return HttpResponse(simplejson.dumps(_update_with_tag_fragments(locals())))
    else:
        return HttpResponseRedirect(reverse("people:person",args=(donor.person.pk,)))


def remove_donor_tag(request, donor_id):
    success = False
    if request.method == "GET":
        tag = request.GET['tag'].strip().lower()
        if tag != "":
            donor = Donor.objects.get(pk=donor_id)
            donor.tags.remove(tag)
            success = True

    if request.is_ajax():
        return HttpResponse(simplejson.dumps(_update_with_tag_fragments(locals())))
    else:
        return HttpResponseRedirect(reverse("people:person",args=(donor.person.pk,)))

@json_view
def new_tag_search_results(request):
    all_tags = False
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            all_tags = Donor.tags.filter(name__icontains=q).order_by("name")[:5]
    return {"fragments":{"new_tag_search_results":render_to_string("people/_new_tag_search_results.html", locals())}}