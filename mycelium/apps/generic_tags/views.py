from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from generic_tags.models import TagSet, Tag
from generic_tags.forms import TagSetForm, TagForm

from people.models import Person
from qi_toolkit.helpers import *

def _render_people_tag_tab(context):
    context.update({'new_tagset_form':TagSetForm(account=context["request"].account),})
    return render_to_string("generic_tags/_people_tag_tab.html", RequestContext(context["request"],context))



class TagViews(object):
    TargetModel = Person
    tag_set_id = None
    app_name = "generic_tags"
    new_tag_placeholder = "New tag"
    mode = "checklist" # or "tags"
    target = None
    reverse_string = "people:person"

    def __init__(self, target=None, tag_set_id=None, *args, **kwargs):
        if target:
            self.target = target
        if tag_set_id:
            self.tag_set_id = tag_set_id
            self.tag_set = TagSet.objects.get(account=target.account, pk=tag_set_id)

    @property
    def _namespace_info(self):
        return {
            "tag_set_id": self.tag_set_id,
            "app_name": self.app_name,
            "mode": self.mode,
            "new_tag_placeholder":self.new_tag_placeholder,
        }

    @property
    def _tag_urls(self):
        create_tag_url = reverse("generic_tags:create_tag", args=(self.tag_set_id, self.target.pk))
        search_results_url = reverse("generic_tags:new_tag_search_results", args=(self.tag_set_id, self.target.pk))
        return {
            'create_tag_url':create_tag_url,
            'search_results_url':search_results_url,
        }

    @property
    def _default_redirect_url(self):
        return self.reverse_string

    @property
    def _default_redirect_args(self):
        return (self.target.pk,)

    @property
    def _tags_for_target(self):
        return self.target.tag_set
   
    @property
    def _all_tags_for_tagset(self):
        return self.tag_set.all_tags()

    @property
    def _target_tag_related_info(self):
        my_tags = self._tags_for_target.all()
        all_of_my_type = self._all_tags_for_tagset

        return {'target_tags':{
                "all_tags_of_my_type": all_of_my_type,
                "all_tags_of_my_type_alphabetical_by_name": all_of_my_type,
                "my_tags": my_tags,
                "my_tags_alphabetical_by_name": my_tags,
        }}

    @property
    def tag_render_context(self):
        d = {}
        d.update(self._tag_urls)
        d.update(self._namespace_info)
        d.update({
            'target':self.target,
        })
        # d.update(self._target_tag_related_info)
        if self.mode == "checklist":
            d.update({"target_tags":self.tag_set.all_tags_with_users_tags_marked(self.target)})

        return d




    def _update_with_tag_fragments(self, context):
        fragment_html = ""

        context.update(self.tag_render_context)

        if self.mode == "tags":
            fragment_html = {"%s_tags" % self.tag_set_id: render_to_string("generic_tags/_tag_list.html", RequestContext(context["request"],context)),}
        elif self.mode == "checklist":
            # This line gets the model of the class, then pulls the tag attribute off of it, and finally gets all tags.
            fragment_html = {"%s_tags" % self.tag_set_id: render_to_string("generic_tags/_tag_checklist.html", RequestContext(context["request"],context)),}
        c = {
            "fragments":fragment_html,
            "success": context["success"],
        }
        return c


    def _return_fragments_or_redirect(self, request, context):
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(self._update_with_tag_fragments(context)))
        else:
            return HttpResponseRedirect("%s#current_detail_tab=%%23tags" % reverse(self._default_redirect_url,args=self._default_redirect_args))


    def create_tag(self, request, tag_set_id, target_id):
        success = False
        self.__init__(target=self.TargetModel.objects_by_account(request).get(pk=int(target_id)), tag_set_id=tag_set_id)
        new_tag = request.REQUEST['new_tag'].strip().lower()
        if new_tag != "":
            ts = TagSet.objects_by_account(request).get(pk=tag_set_id)
            person = Person.objects_by_account(request).get(pk=target_id)
            t = Tag.create_new_tag(tagset=ts,name=new_tag)
            t.add_tag_to_person(person)
            success = True

        return self._return_fragments_or_redirect(request,locals())

    def add_tag(self, request, tag_set_id, tag_id, target_id):
        self.__init__(target=self.TargetModel.objects_by_account(request).get(pk=int(target_id)), tag_set_id=tag_set_id)
        success = False
        t = Tag.objects_by_account(request).get(pk=tag_id)
        person = Person.objects_by_account(request).get(pk=target_id)
        t.add_tag_to_person(person)
        success = True
        return self._return_fragments_or_redirect(request,locals())

    def remove_tag(self, request, tag_set_id, tag_id, target_id):
        self.__init__(target=self.TargetModel.objects_by_account(request).get(pk=int(target_id)), tag_set_id=tag_set_id)
        success = False
        t = Tag.objects_by_account(request).get(pk=tag_id)
        person = Person.objects_by_account(request).get(pk=target_id)
        t.remove_tag_from_person(person=person)
        success = True
        return self._return_fragments_or_redirect(request,locals())
        
    def new_tag_search_results(self, request, tag_set_id, target_id):
        self.__init__(target=self.TargetModel.objects_by_account(request).get(pk=int(target_id)), tag_set_id=tag_set_id)
        all_tags = False
        if 'q' in request.GET:
            q = request.GET['q']
            if q != "":
                all_tags = self._all_tags_for_tagset.filter(name__icontains=q).order_by("name")[:5]
        return HttpResponse(simplejson.dumps({"fragments":{"new_%s_tag_search_results" % self._tag_set_id:render_to_string("generic_tags/_new_tag_search_results.html", locals())}}))

tag_views = TagViews()


#  Normal views
def _tab_or_manage_tags_redirect(context):
    request = context["request"]
    context["all_tagsets"] = TagSet.objects_by_account(request).all()

    if request.is_ajax():
        fragment_html = {"tagset_details" : render_to_string("generic_tags/_manage_tags_tagset_details.html", RequestContext(request,context)),}
        c = {
            "fragments":fragment_html,
            "success": context["success"],
        }
        return HttpResponse(simplejson.dumps(c))
    else:
        return HttpResponseRedirect(reverse("generic_tags:manage"))




def save_tags_and_tagsets(request):
    success = False
    if request.method == "POST":
        data = request.POST

        tagset_forms = [ts.form(data, account=request.account) for ts in TagSet.objects_by_account(request).all()]
        tag_forms = [t.form(data, prefix="TAG-%s" % t.pk, instance=t, account=request.account) for t in Tag.objects_by_account(request).all()]

        # process tagset forms
        for f in tagset_forms:
            if f.is_valid():
                f.save()

        # process tag forms
        for f in tag_forms:
            if f.is_valid():
                f.save()
        
        success = True

    return _tab_or_manage_tags_redirect(locals())


def new_tagset(request):
    success = False
    TagSet.raw_objects.create(account=request.account)
    success = True
    return _tab_or_manage_tags_redirect(locals())

def new_tag(request, tagset_id):
    success = False
    ts = TagSet.objects_by_account(request).get(pk=tagset_id)
    # ts.add
    Tag.raw_objects.create(account=request.account, tagset=ts)
    return _tab_or_manage_tags_redirect(locals())

def delete_tagset(request, tagset_id):
    success = False
    ts = TagSet.objects_by_account(request).get(pk=int(tagset_id))
    ts.delete()
    success = True
    return _tab_or_manage_tags_redirect(locals())

def delete_tag(request, tag_id):
    success = False
    t = Tag.objects_by_account(request).get(pk=int(tag_id))
    t.delete()
    success = True
    return _tab_or_manage_tags_redirect(locals())

@render_to("generic_tags/manage.html")
def manage(request):
    section = "more"
    all_tagsets = TagSet.objects_by_account(request).all()
    return locals()