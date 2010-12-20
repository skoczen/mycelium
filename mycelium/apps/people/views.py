from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page


@render_to("people/search.html")
def search(request):
    return locals()


@render_to("people/person.html")
def person(request):
    return locals()
