from django import forms
from rewrite.models import RewriteWebsite, RewriteTemplate, RewriteSection,  RewriteBlog, RewritePage, RewriteBlogPost

class RewriteWebsiteForm(forms.ModelForm):
    class Meta:
        model = RewriteWebsite
        fields = ("blog_enabled",)

class RewriteSectionForm(forms.ModelForm):
    class Meta:
        model = RewriteSection
        fields = ("name", )

class RewriteTemplateForm(forms.ModelForm):
    class Meta:
        model = RewriteTemplate
        fields = ("name", "extra_head_html", "page_header_html", 
                  "pre_content_html", "post_content_html",
                  "show_main_nav", "show_section_nav",)

class RewriteBlogForm(forms.ModelForm):
    class Meta:
        model = RewriteBlog
        fields = ("template", )


class RewritePageForm(forms.ModelForm):
    class Meta:
        model = RewritePage
        fields = ("title", "section", "nav_link_name", "description", "keywords", "template", "content", "is_published")

class RewriteNewPageForm(forms.ModelForm):
    class Meta:
        model = RewritePage
        fields = ("title", "section", "template",)
    
    def __init__(self, *args, **kwargs):
        super(RewriteNewPageForm,self).__init__(*args,**kwargs)
        self.fields["template"].choices = [f for f in self.fields["template"].choices][1:]


class RewriteBlogPostForm(forms.ModelForm):
    class Meta:
        model = RewriteBlogPost
        fields = ("title", "description", "keywords", "content", "is_published")

class RewriteNewBlogPostForm(forms.ModelForm):
    class Meta:
        model = RewriteBlogPost
        fields = ("title", )
