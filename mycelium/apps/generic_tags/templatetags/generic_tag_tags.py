from django import template
from django.conf import settings
register = template.Library()
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from generic_tags.views import TagViews
from django.db.models import get_model



def _render_tags_context(obj, tag_set_name):
    tv = TagViews(target=obj,tag_set_name=tag_set_name)
    d = tv.tag_render_context
    d.update({
        'MEDIA_URL':settings.MEDIA_URL,
    })

    return d

# @register.inclusion_tag('generic_tags/_tags_and_add_tag.html')
# def render_tags_and_add_tag(obj, tag_set_name):
#     return _render_tags_context(obj, tag_set_name)

@register.inclusion_tag('generic_tags/_js.html')
def generic_tags_js():
    MEDIA_URL = settings.MEDIA_URL
    return locals()

@register.inclusion_tag('generic_tags/_tags_as_checklist.html')
def render_tags_as_checklist(obj, tag_set_name, include_new=True):
    return _render_tags_context(obj, tag_set_name)