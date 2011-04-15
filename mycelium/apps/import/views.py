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
from test_factory import Factory

@render_to("import/list.html")
def list(request):
    # TODO: this is obnoxious.  Fix it.
    section = "more"
    return locals()

@render_to("import/start.html")
def start(request):
    # TODO: this is obnoxious.  Fix it.
    section = "more"
    return locals()

@render_to("import/review.html")
def review(request, import_id):
    # TODO: this is obnoxious.  Fix it.
    section = "more"
    return locals()
