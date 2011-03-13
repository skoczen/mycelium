from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

@render_to("mycelium_core/more_menu.html")
def more_menu(request):
    section = "more"
    return locals()

@render_to("mycelium_core/more_menu.html")
def always_500(request):
    assert True == "This page loaded!"

@render_to("502.html")
def always_502(request):
    return {}