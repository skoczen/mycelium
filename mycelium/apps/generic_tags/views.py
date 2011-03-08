from django.template import RequestContext
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse


class TagViews(object):
    TargetModel = None
    fragment_name = None
    default_redirect_url = None
    default_redirect_args = None

    def _TargetModel(self):
        if self.TargetModel:
            return self.TargetModel
        else:
            raise "_get_model_tag_field not defined!"
        # return Model
    
    def _fragment_name(self):
        if self.fragment_name:
            return self.fragment_name
        else:
            raise "_fragment_name not defined!"

    def _default_redirect_url(self):
        if self.default_redirect_url:
            return self.default_redirect_url
        else:
            raise "_default_redirect_url not defined!"

    def _default_redirect_args(self):
        if self.default_redirect_args:
            return self.default_redirect_args
        else:
            raise "_default_redirect_url not defined!"

    def _update_with_tag_fragments(self, context):
        c = {
            "fragments":{self._fragment_name(): render_to_string("generic_tags/_tag_list.html", RequestContext(context["request"],context)),},
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
                obj.tags.add(new_tag)
                success = True

        return self._return_fragments_or_redirect(request,locals())

    def remove_tag(self, request, target_id):
        success = False
        if request.method == "GET":
            tag = request.GET['tag'].strip().lower()
            if tag != "":
                obj = self._TargetModel().objects.get(pk=target_id)
                obj.tags.remove(tag)
                success = True
        return self._return_fragments_or_redirect(request,locals())


    def new_tag_search_results(request):
        all_tags = False
        if 'q' in request.GET:
            q = request.GET['q']
            if q != "":
                all_tags = self._TargetModel().tags.filter(name__icontains=q).order_by("name")[:5]
        return HttpResponse(simplejson.dumps({"fragments":{"new_tag_search_results":render_to_string("generic_tags/_new_tag_search_results.html", locals())}}))