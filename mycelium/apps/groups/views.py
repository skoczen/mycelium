from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from groups.models import Group
from groups.forms import GroupForm

def _render_people_group_tab(context):
    return render_to_string("groups/_people_group_tab.html", RequestContext(context["request"],context))



def _basic_forms(group, request):
    data = None
    if request.method == "POST":
        data = request.POST
    return GroupForm(data, instance=group)

@render_to("groups/group.html")
def group(request, group_id):
    group = Group.objects.get(pk=group_id)
    form = _basic_forms(group, request)
    return locals()

@json_view
def save_basic_info(request, group_id):
    group = Group.objects.get(pk=group_id)
    form = _basic_forms(group, request)
    success = False
    if form.is_valid():
        group = form.save()
        success = True

    return {"success":success}


def new_group(request):
    group = Group.objects.create(name="Unnamed Group")
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

