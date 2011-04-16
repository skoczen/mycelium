from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page
from django.core.cache import cache

from rules.models import LeftSide, Operator, RightSideType

@render_to("rules/rules_logic.js")
def rules_logic_js(request):
    left_sides = LeftSide.objects_by_account(request).all()
    operators = Operator.objects_by_account(request).all()
    right_side_types = RightSideType.objects_by_account(request).all()
    return locals()