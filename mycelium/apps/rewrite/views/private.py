from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from rewrite.models import RewriteSection, RewriteBlogPost, RewriteTemplate, RewriteWebsite, RewriteBlog
from rewrite.forms import *

def _get_website(request):
    return RewriteWebsite.objects.all()[0]

@login_required
def pages(request):
    tab = "pages"
    website = _get_website(request)

    sections = RewriteSection.objects.all()
    new_page_form = RewriteNewPageForm()
    new_section_form = RewriteSectionForm()
    
    return render_to_response("rewrite/manage/pages.html", locals(), RequestContext(request))

@login_required
def blog(request):
    tab = "blog"
    website = _get_website(request)

    blog_posts = RewriteBlogPost.objects.all()
    blog = RewriteBlog.objects.all()[0]
    new_blog_post_form = RewriteNewBlogPostForm()
    return render_to_response("rewrite/manage/blog.html", locals(), RequestContext(request))

@login_required
def templates(request):
    tab = "templates"
    website = _get_website(request)

    templates = RewriteTemplate.objects.all()
    new_template_form = RewriteTemplateForm()
    return render_to_response("rewrite/manage/templates.html", locals(), RequestContext(request))

@login_required
def settings(request):
    tab = "settings"
    website = _get_website(request)
    blog = RewriteBlog.objects.all()[0]
    if request.method == "POST":
        blog_settings_form = RewriteBlogForm(request.POST, instance=blog)
        website_settings_form = RewriteWebsiteForm(request.POST, instance=website)    
        if blog_settings_form.is_valid() and website_settings_form.is_valid():
            blog_settings_form.save()
            website_settings_form.save()
    else:
        blog_settings_form = RewriteBlogForm(instance=blog)
        website_settings_form = RewriteWebsiteForm(instance=website)

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

@login_required
def save_page(request, page_id):
    success = False
    try:
        assert request.is_ajax() and request.method == "POST" and "content" in request.POST
        website = _get_website(request)
        page = get_object_or_404(RewritePage, pk=page_id, website=website)
        content = request.POST["content"]
        page.content = content
        page.save()
        success = True
    except:
        pass
        
    return HttpResponse(simplejson.dumps({"success":success}))

@login_required
def save_post(request, post_id):
    success = False
    try:
        assert request.is_ajax() and request.method == "POST" and "content" in request.POST
        website = _get_website(request)
        post = get_object_or_404(RewriteBlogPost, pk=post_id, website=website)
        content = request.POST["content"]
        post.content = content
        post.save()
        success = True
    except:
        pass
        
    return HttpResponse(simplejson.dumps({"success":success}))


@login_required
def edit_template(request, template_id):
    tab = "templates"
    website = _get_website(request)
    template = get_object_or_404(RewriteTemplate, pk=template_id, website=website)
    if request.method == "POST":
        template_form = RewriteTemplateForm(request.POST, instance=template)
        if template_form.is_valid():
            template = template_form.save()
    else:
        template_form = RewriteTemplateForm(instance=template)
    
    return render_to_response("rewrite/manage/edit_template.html", locals(), RequestContext(request))
    



@login_required
def delete_page(request, page_id):
    website = _get_website(request)
    page = get_object_or_404(RewritePage, pk=page_id, website=website)
    page.delete()
    return HttpResponseRedirect(reverse("rewrite:manage_pages"))
    
@login_required
def delete_post(request, post_id):
    website = _get_website(request)
    post = get_object_or_404(RewriteBlogPost, pk=post_id, website=website)
    post.delete()
    return HttpResponseRedirect(reverse("rewrite:manage_blog"))

@login_required
def delete_template(request, template_id):
    website = _get_website(request)
    template = get_object_or_404(RewriteTemplate, pk=template_id, website=website)
    template.delete()
    return HttpResponseRedirect(reverse("rewrite:manage_templates"))