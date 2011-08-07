from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

@login_required
def pages(request):
    return render_to_response("rewrite/manage/pages.html", locals(), RequestContext(request))

@login_required
def template(request):
    return render_to_response("rewrite/manage/template.html", locals(), RequestContext(request))

@login_required
def blog(request):
    return render_to_response("rewrite/manage/blog.html", locals(), RequestContext(request))

@login_required
def settings(request):
    return render_to_response("rewrite/manage/settings.html", locals(), RequestContext(request))
