from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
# from django.http import HttpResponseRedirect, HttpResponse
# from django.core.urlresolvers import reverse
# from django.views.decorators.cache import cache_page
# from django.contrib.sites.models import Site
# from django.conf import settings

from rewrite import ContentNotFound
from rewrite.models import RewritePage, RewriteSection, RewriteBlogPost

def page(request, section=None, page_name=None):
    if page_name:
        page = get_object_or_404(RewritePage,slug=page_name)
        template = page.template
        section = page.section

    else:
        if section:
            section = get_object_or_404(RewriteSection,slug=section)
        else:
            raise ContentNotFound

    return render_to_response("rewrite/page.html", locals(), RequestContext(request))

def blog_home(request):
    
    return render_to_response("rewrite/base.html", locals(), RequestContext(request))

def blog_entry(request, entry_slug):
    blog_post = get_object_or_404(RewriteBlogPost,slug=entry_slug)

    return render_to_response("rewrite/base.html", locals(), RequestContext(request))