from django.db import models
from rewrite import DEFAULT_CONTENT_FILLER
from django.template.defaultfilters import slugify
import datetime

class RewriteWebsite(models.Model):
    name                = models.CharField(max_length=255, blank=True, null=True)
    blog_enabled        = models.BooleanField(default=True)
    domain              = models.CharField(max_length=255, blank=True, null=True, verbose_name="Website URL to host (ie. example.com)")

    @property
    def sections(self):
        return self.rewritesection_set.all()

    @property
    def blog(self):
        return self.rewriteblog_set.all()[0]

    @property
    def pages(self):
        return self.rewritepage_set.all()

    def __unicode__(self):
        return "%s" % self.name

class RewriteSection(models.Model):
    name            = models.CharField(max_length=255, blank=True, null=True)
    slug            = models.SlugField(editable=False, blank=True)
    website         = models.ForeignKey(RewriteWebsite)
    order           = models.IntegerField(default=0)
    
    @property
    def pages(self):
        return self.rewritepage_set.all()

    def __unicode__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(RewriteSection, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ("order", "name")
    
    @property
    def first_page(self):
        try:
            return self.pages[0]
        except:
            return None

class RewriteTemplate(models.Model):
    name                = models.CharField(max_length=255, blank=True, null=True)
    page_header_html    = models.TextField(blank=True, null=True, default="<!-- Enter any HTML that should show above the navigation (like a page header) here. -->")
    pre_content_html    = models.TextField(blank=True, null=True, default="<!-- Enter any HTML that goes before the content here -->")
    post_content_html   = models.TextField(blank=True, null=True, default="<!-- Type any HTML that goes after the content here -->")
    extra_head_html     = models.TextField(blank=True, null=True, default="<!-- Enter any JavaScript or CSS that should be in the page <HEAD> here. -->")
    show_main_nav       = models.BooleanField(default=True)
    show_section_nav    = models.BooleanField(default=True)
    website             = models.ForeignKey(RewriteWebsite)

    @property
    def in_use(self):
        return self.rewritepage_set.count() > 0 or self.rewriteblog_set.count() > 0

    def __unicode__(self):
        return "%s" % self.name

    class Meta:
        ordering = ("name",)

class RewriteBlog(models.Model):
    template        = models.ForeignKey(RewriteTemplate, verbose_name="Blog Template")
    website         = models.ForeignKey(RewriteWebsite)

    @property
    def posts(self):
        return self.rewriteblogpost_set.all()


class RewriteContentBase(models.Model):
    title           = models.CharField(max_length=69, verbose_name="Title", blank=True, null=True,
                        help_text="This will show at the top of the browser window, and in search engine results. Less than 70 characters.")
    description     = models.CharField(max_length=156, verbose_name="Page Description", blank=True, null=True,
                        help_text="This text is just for search engines. It will be displayed under your title in the results. Less than 156 characters.")
    keywords        = models.CharField(max_length=255, verbose_name="Keywords", blank=True, null=True,
                        help_text="Keywords help search engines find results. Enter ones that describe this page. Less than 255 characters.")    
    content         = models.TextField(blank=True, null=True, default=DEFAULT_CONTENT_FILLER)
    slug            = models.SlugField(editable=False, blank=True)
    publish_date    = models.DateTimeField(blank=True, null=True)
    is_published    = models.BooleanField(default=False)
    website         = models.ForeignKey(RewriteWebsite)

    def save(self, *args, **kwargs):
        # only do this once - cool URL's don't change.

        if self.id and self.is_published:
            old_me = self.__class__.objects.get(pk=self.id)
            if not old_me.is_published:
                self.slug = slugify(self.title)
                self.publish_date = datetime.datetime.now()
        elif not self.is_published or not self.id:
            self.slug = slugify(self.title)

        super(RewriteContentBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True
    
    def __unicode__(self):
        return "%s" % self.title

class RewritePage(RewriteContentBase):
    section         = models.ForeignKey(RewriteSection, blank=True, null=True)
    template        = models.ForeignKey(RewriteTemplate, blank=False)
    nav_link_name   = models.CharField(max_length=255, verbose_name="Navigation link", blank=True, null=True,
                        help_text="A short name that will be displayed in the section navigation.")
    order           = models.IntegerField(default=0)
    

    def save(self, *args, **kwargs):
        # only do this once - cool URL's don't change.

        if not self.nav_link_name:
            self.nav_link_name = self.title

        super(RewritePage, self).save(*args, **kwargs)


    class Meta:
        ordering = ("order", "title")
    
    @property
    def is_page(self):
        return True
    
    @property
    def is_post(self):
        return False

class RewriteBlogPost(RewriteContentBase):
    blog            = models.ForeignKey(RewriteBlog)

    @property
    def is_page(self):
        return False
    
    @property
    def is_post(self):
        return True
