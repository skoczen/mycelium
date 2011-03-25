from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from qi_toolkit.helpers import *
from django.views.decorators.cache import cache_page
from generic_tags.views import TagViews

from groups.models import Group, GroupMembership, SmartGroup
from people.models import Person

class GroupTagViews(TagViews):
    TargetModel = Person
    namespace_name = "groups"
    default_redirect_url = "people:person"
    app_name = "groups"
    tag_field = "groups"
    mode = "checklist"
    new_tag_placeholder = "New Group"
    def _default_redirect_args(self, context):
        return (context["obj"].pk,)

    def _tags_for_obj(self,obj):
        return obj.groups
    
    def _tags_for_category_and_obj(self, cls, obj):
        all_tags = Group.objects.order_by("name")
        my_tags = obj.groups.order_by("name")

        combined_list = []
        for t in all_tags.all():
            d = {'tag':t}
            if t in my_tags:
                d["have_tag"] = True
            combined_list.append(d)
        return combined_list

    def obj_tag_related_info(self, obj, tag_field=None):
        if tag_field:
            self.tag_field = tag_field
        
        my_tags = self._tags_for_obj(obj)
        all_of_my_type = Group.objects.all()

        return {'obj_tags':{
                "all_tags_of_my_type": all_of_my_type,
                "all_tags_of_my_type_alphabetical_by_name": all_of_my_type.order_by("name"),
                "my_tags": my_tags,
                "my_tags_alphabetical_by_name": my_tags.order_by("name"),
        }}

    def add_tag(self,request):
        success = False
        pk = int(request.REQUEST['target_pk'])
        new_tag = request.REQUEST['new_tag'].strip()
        if new_tag != "":
            obj = Person.objects.get(pk=pk)
            obj.add_group(new_tag)
            success = True

        return self._return_fragments_or_redirect(request,locals())

    def remove_tag(self, request, target_id):
        success = False
        if request.method == "GET":
            tag = request.GET['tag'].strip()
            if tag != "":
                obj = self._TargetModel().objects.get(pk=target_id)
                obj.remove_group(tag)
                success = True
        return self._return_fragments_or_redirect(request,locals())


    def new_tag_search_results(self, request):
        all_tags = False
        if 'q' in request.GET:
            q = request.GET['q']
            if q != "":
                all_tags = Group.objects.filter(name__icontains=q).order_by("name")[:5]
        return HttpResponse(simplejson.dumps({"fragments":{"new_%s_tag_search_results" % self._namespace_name():render_to_string("generic_tags/_new_tag_search_results.html", locals())}}))

tag_views = GroupTagViews()

def _render_people_group_tab(context):
    context.update({"tag_view_obj":tag_views})
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
    smart_group = SmartGroup.objects.create()
    return HttpResponseRedirect("%s?edit=ON" %reverse("groups:smart_group",args=(smart_group.pk,)))

def delete_smart_group(request):
    try:
        if request.method == "POST":
            pk = request.POST['smart_group_pk']
            smart_group = SmartGroup.objects.get(pk=pk)
            smart_group.delete()
    except:
        pass

    return HttpResponseRedirect(reverse("people:search"))
