from django.template import RequestContext
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from rewrite.models import RewriteSection, RewriteBlogPost, RewriteTemplate

@login_required
def pages(request):
    tab = "pages"
    sections = RewriteSection.objects.all()
    return render_to_response("rewrite/manage/pages.html", locals(), RequestContext(request))

@login_required
def blog(request):
    tab = "blog"
    blog_posts = RewriteBlogPost.objects.all()
    return render_to_response("rewrite/manage/blog.html", locals(), RequestContext(request))

@login_required
def templates(request):
    tab = "templates"
    templates = RewriteTemplate.objects.all()
    return render_to_response("rewrite/manage/templates.html", locals(), RequestContext(request))

@login_required
def settings(request):
    tab = "settings"
    return render_to_response("rewrite/manage/settings.html", locals(), RequestContext(request))
