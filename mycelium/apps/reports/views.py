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
import random

@render_to("reports/search.html")
def search(request):
    # reports = Report.objects.all()
    return locals()

@render_to("reports/detail.html")
def detail(request, report_id):
    # report = get_object_or_404(Report, report_id)
    five_people = Person.objects.order_by("?").all()[:5]
    hours = [random.randint(2,280) for i in range(0,5)]
    return locals()