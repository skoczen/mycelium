from django.template import RequestContext
from django.conf import settings
from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

def _render_people_recent_activity_tab(context):
    return render_to_string("recent_activity/_people_recent_activity_tab.html", RequestContext(context["request"],context))
