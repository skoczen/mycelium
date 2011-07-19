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
from people.models import Person
from organizations.models import Organization
from donors.models import Donation
from volunteers.models import CompletedShift
from generic_tags.models import Tag, TaggedItem
import datetime

@render_to("flight_control/home.html")
def home(request):
    section = "dashboard"

    
    return {}

@json_view
def search_results(request):
    pass