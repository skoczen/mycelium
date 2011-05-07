from django.template import RequestContext
from django.template.loader import render_to_string
from accounts.managers import get_or_404_by_account
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from django.db.models import Sum, Count, Avg

from groups.models import Group
from people.models import Person, Organization
from donors.models import Donation
from volunteers.models import CompletedShift
from generic_tags.models import Tag, TaggedItem
import datetime
from decimal import Decimal

def _account_numbers_dict(account):
    start_of_this_year = datetime.date(month=1, day=1, year=datetime.date.today().year)
    
    total_donations = int(Donation.objects_by_account(account).filter(date__gte=start_of_this_year).count())
    total_donors = int(Donation.objects_by_account(account).filter(date__gte=start_of_this_year).order_by().all().aggregate(Count('donor', distinct=True))["donor__count"])
    total_donation_amount = Decimal(Donation.objects_by_account(account).filter(date__gte=start_of_this_year).order_by().all().aggregate(Sum('amount'))["amount__sum"])
    average_donation = Decimal(Donation.objects_by_account(account).filter(date__gte=start_of_this_year).order_by().all().aggregate(Avg('amount'))["amount__avg"])
    total_volunteer_hours = int(CompletedShift.objects_by_account(account).filter(date__gte=start_of_this_year).order_by().all().aggregate(Sum('duration'))["duration__sum"])
    total_people = Person.objects_by_account(account).count()
    total_orgs = Organization.objects_by_account(account).count()
    total_groups = Group.objects_by_account(account).count()
    total_tags = Tag.objects_by_account(account).count()
    total_taggeditems = TaggedItem.objects_by_account(account).count()

    return locals()


@render_to("dashboard/dashboard.html")
def dashboard(request):
    section = "dashboard"

    if not request.account.has_completed_all_challenges:
        request.account.check_challenge_progress()
    
    d = _account_numbers_dict(request.account)
    d.update({'request':request, 'section':section})
    return d

@json_view
def save_nickname(request):
    success = False
    if "nickname" in request.POST:
        me = request.useraccount
        me.nickname = request.POST["nickname"]
        me.save()
        success = True

    return {'success':success}