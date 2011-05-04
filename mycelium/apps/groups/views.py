from django.template import RequestContext
from django.template.loader import render_to_string
from accounts.managers import get_or_404_by_account
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page

from groups.models import Group
from groups.forms import GroupForm, GroupRuleFormset
from people.models import PeopleAndOrganizationsSearchProxy

def _render_people_group_tab(context):
    return render_to_string("groups/_people_group_tab.html", RequestContext(context["request"],context))



def _basic_forms(group, request, no_data=False):
    data = None
    if not no_data and request and request.method == "POST":
        data = request.POST
    
    account = request.account
    group_form = GroupForm(data, instance=group, account=account)
    rule_formset = GroupRuleFormset(data, instance=group, account=account)
    return group_form, rule_formset

@render_to("people/search.html")
def search(request):
    section = "groups"
    people_proxies = PeopleAndOrganizationsSearchProxy.objects_by_account(request.account).exclude(group__isnull=True).all()
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            people_proxies = PeopleAndOrganizationsSearchProxy.search(request.account, q,ignorable_chars=["-","(",")"]).exclude(group__isnull=True)
    return locals()

@json_view
def search_results(request):
    section = "groups"
    people_proxies = PeopleAndOrganizationsSearchProxy.objects_by_account(request.account).exclude(group__isnull=True).all()
    if 'q' in request.GET:
        q = request.GET['q']
        if q != "":
            people_proxies = PeopleAndOrganizationsSearchProxy.search(request.account, q,ignorable_chars=["-","(",")"]).exclude(group__isnull=True)

    return {"fragments":{"main_search_results":render_to_string("people/_search_results.html", locals())}}



@render_to("groups/group.html")
def group(request, group_id):
    group = get_or_404_by_account(Group, request.account, group_id)
    members = group.members
    form, rule_formset = _basic_forms(group, request)
    return locals()

@json_view
def save_basic_info(request, group_id):
    group = get_or_404_by_account(Group, request.account, group_id, using='default')
    form, rule_formset = _basic_forms(group, request)
    success = False

    if rule_formset.is_valid():
        rule_formset.save()

    if form.is_valid():
        group = form.save()
        success = True

    form, rule_formset = _basic_forms(group, request, no_data=True)

    return {"success":success}



def new_group(request):
    group = Group.raw_objects.using('default').create(account=request.account)
    return HttpResponseRedirect("%s?edit=ON" %reverse("groups:group",args=(group.pk,)))
    

def delete_group(request):
    try:
        if request.method == "POST":
            pk = request.POST['group_pk']
            group = get_or_404_by_account(Group, request.account, pk, using='default')
            group.delete()
    except:
        pass

    return HttpResponseRedirect(reverse("people:search"))

@json_view
def group_members_partial(request, group_id):
    group = get_or_404_by_account(Group, request.account, group_id)
    members = group.members.using('default')
    return {
    "fragments":{
        "group_member_count":render_to_string("groups/_group_member_count.html", locals()),
        "group_member_list":render_to_string("groups/_group_member_list.html", locals())
            }
    }