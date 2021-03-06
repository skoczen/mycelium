from django.template import RequestContext
from django.conf import settings
from django.shortcuts import render_to_response
from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from logo_maker.models import Logo
from logo_maker.forms import LogoForm

from django.forms.formsets import formset_factory
from sorl.thumbnail import get_thumbnail

@render_to("logo_maker/list.html")
def list_logos(request):
    section = "admin"
    if request.method == "POST":
        form = LogoForm(request.POST, request.FILES, account=request.account)
        if form.is_valid():
            form.save()
            form = LogoForm(account=request.account)
        else: 
            print "not_valid"
            print form.__dict__
    else:
        form = LogoForm(account=request.account)

    logos = Logo.objects_by_account(request.account).all()
    return locals()


def download_resized(request, logo_id):
    logo = get_or_404_by_account(Logo, request.account, logo_id)
    width = int(request.GET['width'])
    height = int(request.GET['height'])
    w_by_h = "%sx%s" %(width,height)
    if "crop" in request.GET:
        im = get_thumbnail(logo.image, w_by_h, crop='center')
    else:
        im = get_thumbnail(logo.image, w_by_h, )
    return HttpResponseRedirect(im.url)
    # return HttpResponse(im.read(), mimetype='image/png')
