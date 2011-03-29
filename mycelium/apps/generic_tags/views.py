from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from generic_tags.models import TagSet, TagSetMembership
from generic_tags.forms import TagSetForm
from people.models import Person

def _render_people_tag_tab(context):
    context.update({'new_tagset_form':TagSetForm(),})
    return render_to_string("generic_tags/_people_tag_tab.html", RequestContext(context["request"],context))



class TagViews(object):
    TargetModel = Person
    tag_set_name = None
    app_name = "generic_tags"
    new_tag_placeholder = "New tag"
    mode = "checklist" # or "tags"
    target = None
    reverse_string = "people:person"

    def __init__(self, target=None, tag_set_name=None, *args, **kwargs):
        if target:
            self.target = target
            if tag_set_name:
                self.tag_set_name = tag_set_name
                self.tag_set = TagSet.objects.get(slug__iexact=self.tag_set_name)
                self.tag_set_membership = TagSetMembership.objects.get_or_create(person=self.target,tagset=self.tag_set)[0]

    @property
    def _namespace_info(self):
        return {
            "tag_set_name": self.tag_set_name,
            "app_name": self.app_name,
            "mode": self.mode,
            "new_tag_placeholder":self.new_tag_placeholder,
        }

    @property
    def _tag_urls(self):
        add_tag_url = reverse("generic_tags:add_tag", args=(self.tag_set_name, self.target.pk))
        delete_tag_url = reverse("generic_tags:remove_tag", args=(self.tag_set_name, self.target.pk))
        search_results_url = reverse("generic_tags:new_tag_search_results", args=(self.tag_set_name, self.target.pk))
        return {
            'add_tag_url':add_tag_url,
            'delete_tag_url':delete_tag_url,
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
        return self.tag_set_membership.tags
   
    @property
    def _all_tags_for_tagset(self):
        return self.tag_set.all_tags

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
            'new_tagset_form':TagSetForm(),
        })
        # d.update(self._target_tag_related_info)
        if self.mode == "checklist":
            d.update({"target_tags":self.tag_set_membership.all_tags_with_my_tags_marked})

        return d




    def _update_with_tag_fragments(self, context):
        fragment_html = ""

        context.update(self.tag_render_context)

        if self.mode == "tags":
            fragment_html = {"%s_tags" % self.tag_set_name: render_to_string("generic_tags/_tag_list.html", RequestContext(context["request"],context)),}
        elif self.mode == "checklist":
            # This line gets the model of the class, then pulls the tag attribute off of it, and finally gets all tags.
            fragment_html = {"%s_tags" % self.tag_set_name: render_to_string("generic_tags/_tag_checklist.html", RequestContext(context["request"],context)),}
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


    def add_tag(self,request, tag_set_name, target_id):
        self.__init__(target=self.TargetModel.objects.get(pk=int(target_id)), tag_set_name=tag_set_name)
        success = False
        new_tag = request.REQUEST['new_tag'].strip().lower()
        if new_tag != "":
            self._tags_for_target.add(new_tag)
            success = True

        return self._return_fragments_or_redirect(request,locals())

    def remove_tag(self, request, tag_set_name, target_id):
        success = False
        self.__init__(target=self.TargetModel.objects.get(pk=int(target_id)), tag_set_name=tag_set_name)
        if request.method == "GET":
            tag = request.GET['tag'].strip().lower()
            if tag != "":
                self._tags_for_target.remove(tag)
                success = True
        return self._return_fragments_or_redirect(request,locals())


    def new_tag_search_results(self, request, tag_set_name, target_id):
        self.__init__(target=self.TargetModel.objects.get(pk=int(target_id)), tag_set_name=tag_set_name)
        all_tags = False
        if 'q' in request.GET:
            q = request.GET['q']
            if q != "":
                all_tags = self._all_tags_for_tagset.filter(name__icontains=q).order_by("name")[:5]
        return HttpResponse(simplejson.dumps({"fragments":{"new_%s_tag_search_results" % self._tag_set_name:render_to_string("generic_tags/_new_tag_search_results.html", locals())}}))

    def new_tagset(self, request, target_id):
        success=False
        self.__init__(target=self.TargetModel.objects.get(pk=int(target_id)))
        form = TagSetForm(request.POST)
        if form.is_valid():
            if TagSet.objects.filter(name__iexact=form.cleaned_data["name"]).count() == 0:
                new_tagset = form.save()
            success = True
        return self._return_fragments_or_redirect(request,locals())

tag_views = TagViews()


