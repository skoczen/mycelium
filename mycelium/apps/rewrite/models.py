from django.db import models
from rewrite import DEFAULT_CONTENT_FILLER
from django.template.defaultfilters import slugify

class RewriteWebsite(models.Model):
    name                = models.CharField(max_length=255, blank=True, null=True)
    blog_enabled        = models.BooleanField(default=True)

    @property
    def sections(self):
        return self.rewritesection_set.all()

    def __unicode__(self):
        return "%s" % self.name

class RewriteSection(models.Model):
    name                = models.CharField(max_length=255, blank=True, null=True)
    
    @property
    def pages(self):
        return self.rewritepage_set.all()

    def __unicode__(self):
        return "%s" % self.name

class RewriteTemplate(models.Model):
    name                = models.CharField(max_length=255, blank=True, null=True)
    page_header_html    = models.TextField(blank=True, null=True)
    pre_content_html    = models.TextField(blank=True, null=True)
    post_content_html   = models.TextField(blank=True, null=True)
    extra_head_html     = models.TextField(blank=True, null=True)
    show_main_nav       = models.BooleanField(default=True)
    show_section_nav    = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % self.name

class RewriteBlog(models.Model):
    template        = models.ForeignKey(RewriteTemplate)

    @property
    def posts(self):
        return self.rewriteblogpost_set.all()


class RewriteContentBase(models.Model):
    title           = models.CharField(max_length=69, verbose_name="Page Title", blank=True, null=True,
                        help_text="This will show at the top of the browser window, and in search engine results. Less than 70 characters.")
    description     = models.CharField(max_length=156, verbose_name="Page Description", blank=True, null=True,
                        help_text="This text is just for search engines. It will be displayed under your title in the results. Less than 156 characters.")
    keywords        = models.CharField(max_length=255, verbose_name="Keywords", blank=True, null=True,
                        help_text="Keywords help search engines find results. Enter ones that describe this page. Less than 255 characters.")    
    content         = models.TextField(blank=True, null=True, default=DEFAULT_CONTENT_FILLER)
    slug            = models.SlugField(editable=False, blank=True)
    is_published    = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # only do this once - cool URL's don't change.
        print self.__class__
        if not self.slug or not self.is_published:
            self.slug = slugify(self.title)
        super(RewriteContentBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True
    
    def __unicode__(self):
        return "%s" % self.title

class RewritePage(RewriteContentBase):
    section         = models.ForeignKey(RewriteSection, blank=True, null=True)
    template        = models.ForeignKey(RewriteTemplate)
    nav_link_name   = models.CharField(max_length=255, verbose_name="Navigation link", blank=True, null=True,
                        help_text="A short name that will be displayed in the section Navigation.")

class RewriteBlogPost(RewriteContentBase):
    pass