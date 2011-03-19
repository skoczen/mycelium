from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse


class TagViews(object):
    TargetModel = None
    namespace_name = None
    default_redirect_url = None
    default_redirect_args = None
    app_name = None
    mode = "tags" # or "checklist"

    def _TargetModel(self):
        if self.TargetModel:
            return self.TargetModel
        else:
            raise Exception, "_get_model_tag_field not defined!"
        # return Model

    def _app_name(self):
        if self.app_name:
            return self.app_name
        else:
            raise Exception, "_app_name not defined!"    

    def _namespace_name(self):
        if self.namespace_name:
            return self.namespace_name
        else:
            raise Exception, "_namespace_name not defined!"

    def _tag_field(self):
        if hasattr(self,"tag_field"):
            return self.tag_field
        else:
            return "tags"

    def _tags_for_obj(self,obj):
        return getattr(obj,self._tag_field())
    
    def _tags_for_category_and_obj(self, cls, obj):
        all_tags = self._tags_for_obj(cls).all().order_by("name")
        my_tags = self._tags_for_obj(obj).all().order_by("name")

        combined_list = []
        for t in all_tags.all():
            d = {'tag':t}
            if t in my_tags:
                d["have_tag"] = True
            combined_list.append(d)
        return combined_list

    def _default_redirect_url(self):
        if self.default_redirect_url:
            return self.default_redirect_url
        else:
            raise Exception, "_default_redirect_url not defined!"

    def _default_redirect_args(self, context):
        if self.default_redirect_args:
            return self.default_redirect_args
        else:
            raise Exception, "_default_redirect_url not defined!"

    def all_tags(self):
        return self._tags_for_obj(self._TargetModel()).all()


    @classmethod
    def _cls_tag_urls(cls, app_name, namespace_name, obj):
        add_tag_url = reverse("%s:%sadd_tag" % (app_name, namespace_name))
        delete_tag_url = reverse("%s:%sremove_tag" % (app_name, namespace_name), args=(obj.pk,))
        search_results_url = reverse("%s:%snew_tag_search_results" % (app_name, namespace_name))
        return {
            'add_tag_url':add_tag_url,
            'delete_tag_url':delete_tag_url,
            'search_results_url':search_results_url,
        }

    def _tag_urls(self, obj):
        add_tag_url = reverse("%s:%sadd_tag" % (self.app_name, self.namespace_name))
        delete_tag_url = reverse("%s:%sremove_tag" % (self.app_name, self.namespace_name), args=(obj.pk,))
        search_results_url = reverse("%s:%snew_tag_search_results" % (self.app_name, self.namespace_name))
        return {
            'add_tag_url':add_tag_url,
            'delete_tag_url':delete_tag_url,
            'search_results_url':search_results_url,
        }

    def checklist_tag_related_info(self,obj,tag_field=None):
        return {
            'all_of_my_type_with_obj_tags': self._tags_for_category_and_obj(self._TargetModel(), obj)
        }

    
    def obj_tag_related_info(self, obj, tag_field=None):
        if tag_field:
            self.tag_field = tag_field
        
        my_tags = self._tags_for_obj(obj).all()
        all_of_my_type = self._tags_for_obj(self._TargetModel()).all()

        return {'obj_tags':{
                "all_tags_of_my_type": all_of_my_type,
                "all_tags_of_my_type_alphabetical_by_name": all_of_my_type.order_by("name"),
                "my_tags": my_tags,
                "my_tags_alphabetical_by_name": my_tags.order_by("name"),
        }}

    def namespace_info(self):
        return {
            "namespace_name": self.namespace_name,
            "app_name": self.app_name,
            "mode": self.mode
        }

    def _update_with_tag_fragments(self, context):
        context.update(self._tag_urls(context["obj"]))
        fragment_html = ""
        context.update(self.obj_tag_related_info(context["obj"]))

        if self.mode == "tags":
            fragment_html = {"%s_tags" % self._namespace_name(): render_to_string("generic_tags/_tag_list.html", RequestContext(context["request"],context)),}
        elif self.mode == "checklist":
            context["obj_tags"].update(self.checklist_tag_related_info(context["obj"]))
            # This line gets the model of the class, then pulls the tag attribute off of it, and finally gets all tags.
            fragment_html = {"%s_tags" % self._namespace_name(): render_to_string("generic_tags/_tag_checklist.html", RequestContext(context["request"],context)),}
        c = {
            "fragments":fragment_html,
            "success": context["success"],
        }
        return c


    def _return_fragments_or_redirect(self, request, context):
        if request.is_ajax():
            return HttpResponse(simplejson.dumps(self._update_with_tag_fragments(context)))
        else:
            return HttpResponseRedirect(reverse(self._default_redirect_url(),args=self._default_redirect_args(context)))

    def add_tag(self,request):
        success = False
        if request.method == "POST":
            pk = int(request.POST['target_pk'])
            new_tag = request.POST['new_tag'].strip().lower()
            if new_tag != "":
                obj = self._TargetModel().objects.get(pk=pk)
                self._tags_for_obj(obj).add(new_tag)
                success = True

        return self._return_fragments_or_redirect(request,locals())

    def remove_tag(self, request, target_id):
        success = False
        if request.method == "GET":
            tag = request.GET['tag'].strip().lower()
            if tag != "":
                obj = self._TargetModel().objects.get(pk=target_id)
                self._tags_for_obj(obj).remove(tag)
                success = True
        return self._return_fragments_or_redirect(request,locals())


    def new_tag_search_results(self, request):
        all_tags = False
        if 'q' in request.GET:
            q = request.GET['q']
            if q != "":
                all_tags = self._tags_for_obj(self._TargetModel()).filter(name__icontains=q).order_by("name")[:5]
        return HttpResponse(simplejson.dumps({"fragments":{"new_%s_tag_search_results" % self._namespace_name():render_to_string("generic_tags/_new_tag_search_results.html", locals())}}))