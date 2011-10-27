from django import template
from django.conf import settings
register = template.Library()
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

# @register.inclusion_tag('mycelium_core/template_tags/generic_fields/css.html')
# def head(include_context=True):
#     MEDIA_URL = settings.MEDIA_URL
#     STATIC_URL = settings.STATIC_URL
#     return locals()
# 
# @register.inclusion_tag('mycelium_core/template_tags/generic_fields/javascript.html')
# def render_tag_set(include_context=True):
#     MEDIA_URL = settings.MEDIA_URL
#     STATIC_URL = settings.STATIC_URL
#     return locals()
