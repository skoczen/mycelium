from django import template
from django.conf import settings
register = template.Library()
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string

@register.inclusion_tag('mycelium_core/template_tags/generic_fields/css.html')
def generic_field_css(include_context=True):
    MEDIA_URL = settings.MEDIA_URL
    return locals()

@register.inclusion_tag('mycelium_core/template_tags/generic_fields/javascript.html')
def generic_field_javascript(include_context=True):
    MEDIA_URL = settings.MEDIA_URL
    return locals()


@register.inclusion_tag('mycelium_core/template_tags/generic_fields/editable_field.html')
def generic_editable_field(field, field_type="input",include_context=True):
    MEDIA_URL = settings.MEDIA_URL
    return locals()

@register.inclusion_tag('mycelium_core/template_tags/generic_fields/editable_field.html')
def generic_editable_field_email(field, field_type="input",include_context=True):
    MEDIA_URL = settings.MEDIA_URL
    generic_editable_view_override = render_to_string("mycelium_core/template_tags/generic_fields/_email_view.html",locals())
    return locals()

# @register.inclusion_tag('mycelium_core/template_tags/generic_fields/edit.html')
# def generic_field_edit(include_context=True):
#     MEDIA_URL = settings.MEDIA_URL
#     return locals()


@register.filter
def field_value(field):
    """ 
    Returns the value for this BoundField, as rendered in widgets. 
    """ 
    if not field.form.is_bound: 
        val = field.form.initial.get(field.name, field.field.initial) 
        if callable(val): 
            val = val() 
    else: 
        from django.forms.fields import FileField
        if isinstance(field.field, FileField) and field.data is None: 
            val = field.form.initial.get(field.name, field.field.initial) 
        else: 
            val = field.data 
    if val is None: 
        val = '' 
    return val
