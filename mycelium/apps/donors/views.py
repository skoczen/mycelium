from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response
from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page
from activities.tasks import save_action

from donors.forms import NewDonationForm
from donors.models import Donor, Donation

def _render_people_donor_tab(context):
    donation_form = NewDonationForm(account=context["request"].account)
    context.update({"donation_form":donation_form,"donor":context["person"].donor})
    return render_to_string("donors/_people_donor_tab.html", RequestContext(context["request"],context))

def _return_fragments_or_redirect(request,context):
    if request.is_ajax():
        return HttpResponse(simplejson.dumps( {"fragments":{"detail_tab":_render_people_donor_tab(context)}}))
    else:
        return HttpResponseRedirect(reverse("people:person",args=(context["person"].pk,)))    


def save_new_donation(request, donor_id):
    donor = get_or_404_by_account(Donor, request.account, donor_id, using='default')
    person = donor.person
    obj = donor
    if request.method == "POST":
        form = NewDonationForm(request.POST, account=request.account)
        if form.is_valid():
            new_donation = form.save(commit=False)
            new_donation.donor = donor
            new_donation.save()
            save_action.delay(request.account, request.useraccount, "added a donation", person=person, donation=new_donation)
        else:
            print form
    return _return_fragments_or_redirect(request,locals())

def delete_donation_from_people_tab(request, donation_id):
    d = get_or_404_by_account(Donation, request.account, donation_id, using='default')
    donor = d.donor
    person = donor.person
    d.delete()
    obj = donor

    return _return_fragments_or_redirect(request,locals())
