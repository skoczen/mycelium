from django.db import models

class RewriteWebsite(models.Model):
    name                = models.CharField(max_length=255, blank=True, null=True)
    blog_enabled        = models.BooleanField(default=True)


class RewriteSection(models.Model):
    name                = models.CharField(max_length=255, blank=True, null=True)
    

class RewriteTemplate(models.Model):
    name                = models.CharField(max_length=255, blank=True, null=True)
    page_header_html    = models.TextField(blank=True, null=True)
    pre_content_html    = models.TextField(blank=True, null=True)
    post_content_html   = models.TextField(blank=True, null=True)
    extra_head_html     = models.TextField(blank=True, null=True)
    show_main_nav       = models.BooleanField(default=True)
    show_section_nav    = models.BooleanField(default=True)


class RewriteBlog(models.Model):
    template        = models.ForeignKey(RewriteTemplate)


class RewriteContentBase(models.Model):
    title           = models.CharField(max_length=69, verbose_name="Page Title", blank=True, null=True,
                        help_text="This will show at the top of the browser window, and in search engine results. Less than 70 characters.")
    description     = models.CharField(max_length=156, verbose_name="Page Description", blank=True, null=True,
                        help_text="This text is just for search engines. It will be displayed under your title in the results. Less than 156 characters.")
    keywords        = models.CharField(max_length=255, verbose_name="Keywords", blank=True, null=True,
                        help_text="Keywords help search engines find results. Enter ones that describe this page. Less than 255 characters.")    
    template        = models.ForeignKey(RewriteTemplate)

    content         = models.TextField(blank=True, null=True)

class RewritePage(RewriteContentBase):
    section         = models.ForeignKey(RewriteSection, blank=True, null=True)
    nav_link_name   = models.CharField(max_length=255, verbose_name="Navigation link", blank=True, null=True,
                        help_text="A short name that will be displayed in the section Navigation.")

class RewriteBlogPost(RewriteContentBase):
    pass