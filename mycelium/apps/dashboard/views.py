from django.template import RequestContext
from django.template.loader import render_to_string
from accounts.managers import get_or_404_by_account
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from django.db.models import Sum, Count

from groups.models import Group
from people.models import Person, Organization
from donors.models import Donation
from volunteers.models import CompletedShift
from generic_tags.models import Tag
import datetime


@render_to("dashboard/dashboard.html")
def dashboard(request):
    section = "dashboard"
    start_of_this_year = datetime.date(month=1, day=1, year=datetime.date.today().year)
    total_donors = Donation.objects_by_account(request.account).filter(date__gte=start_of_this_year).order_by().all().aggregate(Count('donor'))
    total_donations = Donation.objects_by_account(request.account).filter(date__gte=start_of_this_year).order_by().all().aggregate(Sum('amount'))
    total_volunteer_hours = CompletedShift.objects_by_account(request.account).filter(date__gte=start_of_this_year).order_by().all().aggregate(Sum('duration'))
    total_people = Person.objects_by_account(request.account).count()
    total_orgs = Organization.objects_by_account(request.account).count()
    total_groups = Group.objects_by_account(request.account).count()
    total_tags = Tag.objects_by_account(request.account).count()

    return locals()
