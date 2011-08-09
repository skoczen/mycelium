from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from rewrite.models import RewriteSection, RewriteBlogPost, RewriteTemplate
from rewrite.forms import RewriteBlogPostForm, RewritePageForm, RewriteSectionForm, RewriteNewPageForm, RewriteTemplateForm, RewriteNewBlogPostForm

@login_required
def pages(request):
    tab = "pages"
    sections = RewriteSection.objects.all()
    new_page_form = RewriteNewPageForm()
    new_section_form = RewriteSectionForm()
    return render_to_response("rewrite/manage/pages.html", locals(), RequestContext(request))

@login_required
def blog(request):
    tab = "blog"
    blog_posts = RewriteBlogPost.objects.all()
    new_blog_post_form = RewriteNewBlogPostForm()
    return render_to_response("rewrite/manage/blog.html", locals(), RequestContext(request))

@login_required
def templates(request):
    tab = "templates"
    templates = RewriteTemplate.objects.all()
    new_template_form = RewriteTemplateForm()
    return render_to_response("rewrite/manage/templates.html", locals(), RequestContext(request))

@login_required
def settings(request):
    tab = "settings"
    return render_to_response("rewrite/manage/settings.html", locals(), RequestContext(request))


@login_required
def new_page(request):
    if request.is_ajax():
        print "ajax"
    else:
        print "normal"
        new_page_form = RewriteNewPageForm(request.POST)
        if new_page_form.is_valid():
            new_page_form.save()
        return HttpResponseRedirect(reverse("rewrite:manage_pages"))
    

@login_required
def new_section(request):
    if request.is_ajax():
        print "ajax"
    else:
        print "normal"
        new_page_form = RewriteSectionForm(request.POST)
        if new_page_form.is_valid():
            new_page_form.save()
        return HttpResponseRedirect(reverse("rewrite:manage_pages"))


@login_required
def new_template(request):
    if request.is_ajax():
        print "ajax"
    else:
        print "normal"
        new_template_form = RewriteTemplateForm(request.POST)
        if new_template_form.is_valid():
            new_template_form.save()
        return HttpResponseRedirect(reverse("rewrite:manage_templates"))


@login_required
def new_blog_post(request):
    if request.is_ajax():
        print "ajax"
    else:
        print "normal"
        new_blog_post_form = RewriteNewBlogPostForm(request.POST)
        if new_blog_post_form.is_valid():
            new_blog_post_form.save()
        return HttpResponseRedirect(reverse("rewrite:manage_blog"))