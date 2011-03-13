from django import template
from django.conf import settings
register = template.Library()
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from generic_tags.views import TagViews

@register.inclusion_tag('generic_tags/_tags_and_add_tag.html')
def render_tags_and_add_tag(obj, app_name="", url_namespace="", tag_field="tags"):
    MEDIA_URL = settings.MEDIA_URL
    c = locals()
    c.update(TagViews._tag_urls(app_name,url_namespace,obj))
    return c

@register.inclusion_tag('generic_tags/_js.html')
def generic_tags_js():
    MEDIA_URL = settings.MEDIA_URL
    return locals()
