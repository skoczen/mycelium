from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page
from django.template.loader import render_to_string

from mycelium_core.models import SearchableItemProxy

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


@json_view
def search_results(request):
    search_proxies = SearchableItemProxy.objects_by_account(request.account).none()
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            search_proxies = SearchableItemProxy.search(request.account, q,ignorable_chars=["-","(",")"])[:6]

    return {"fragments":{"global_search_results":render_to_string("mycelium_core/_search_results.html", locals())}}
