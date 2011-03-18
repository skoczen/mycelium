from django import template
from django.conf import settings
register = template.Library()
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from generic_tags.views import TagViews
from django.db.models import get_model



def _render_tags_context(obj, tag_view_obj):
    d = {
        'MEDIA_URL':settings.MEDIA_URL,
        'obj':obj,
        'tag_view_obj':tag_view_obj,
    }

    d.update(tag_view_obj._tag_urls(obj))
    d.update(tag_view_obj.namespace_info())
    d.update(tag_view_obj.obj_tag_related_info(obj))
    return d

@register.inclusion_tag('generic_tags/_tags_and_add_tag.html')
def render_tags_and_add_tag(obj, tag_view_obj):
    return _render_tags_context(obj, tag_view_obj)

@register.inclusion_tag('generic_tags/_js.html')
def generic_tags_js():
    MEDIA_URL = settings.MEDIA_URL
    return locals()

@register.inclusion_tag('generic_tags/_tags_as_checklist.html')
def render_tags_as_checklist(obj, tag_view_obj, include_new=True):
    return _render_tags_context(obj, tag_view_obj)