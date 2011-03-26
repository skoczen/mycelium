from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from groups.models import Group
from people.models import Person

def _render_people_group_tab(context):
    return render_to_string("groups/_people_group_tab.html", RequestContext(context["request"],context))


@render_to("groups/group.html")
def group(request, group_id):
    group = Group.objects.get(pk=group_id)
    return locals()

def new_group(request):
    group = Group.objects.create()
    return HttpResponseRedirect("%s?edit=ON" %reverse("groups:group",args=(group.pk,)))

def delete_group(request):
    try:
        if request.method == "POST":
            pk = request.POST['group_pk']
            group = Group.objects.get(pk=pk)
            group.delete()
    except:
        pass

    return HttpResponseRedirect(reverse("people:search"))



@render_to("groups/smart_group.html")
def smart_group(request, smart_group_id):
    return locals()

def new_smart_group(request):
    smart_group = Group.objects.create()
    return HttpResponseRedirect("%s?edit=ON" %reverse("groups:smart_group",args=(smart_group.pk,)))

def delete_smart_group(request):
    try:
        if request.method == "POST":
            pk = request.POST['smart_group_pk']
            smart_group = Group.objects.get(pk=pk)
            smart_group.delete()
    except:
        pass

    return HttpResponseRedirect(reverse("people:search"))
