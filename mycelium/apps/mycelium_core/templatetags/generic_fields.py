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


@register.inclusion_tag('mycelium_core/template_tags/generic_fields/plain_editable_field.html')
def plain_editable_field(field, label_override=None, field_type="input",include_context=True):
    MEDIA_URL = settings.MEDIA_URL
    return locals()

@register.inclusion_tag('mycelium_core/template_tags/generic_fields/editable_field_table.html')
def generic_editable_field_table(field, label_override=None, field_type="input",include_context=True):
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

@register.inclusion_tag('mycelium_core/template_tags/generic_fields/editable_field.html')
def generic_editable_field_anyall_bool(field, field_type="input",include_context=True):
    MEDIA_URL = settings.MEDIA_URL
    generic_editable_view_override = render_to_string("mycelium_core/template_tags/generic_fields/_anyall_bool_view.html",locals())
    return locals()



@register.inclusion_tag('mycelium_core/template_tags/generic_fields/editable_field.html')
def generic_editable_field_twitter(field, field_type="input",include_context=True):
    MEDIA_URL = settings.MEDIA_URL
    generic_editable_view_override = render_to_string("mycelium_core/template_tags/generic_fields/_twitter_view.html",locals())
    return locals()


@register.inclusion_tag('mycelium_core/template_tags/generic_fields/editable_field.html')
def generic_editable_field_url(field, field_type="input",include_context=True):
    MEDIA_URL = settings.MEDIA_URL
    generic_editable_view_override = render_to_string("mycelium_core/template_tags/generic_fields/_url_view.html",locals())
    generic_editable_edit_override = render_to_string("mycelium_core/template_tags/generic_fields/_url_edit.html",locals())    
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

    from django.forms.fields import ChoiceField
    if isinstance(field.field, ChoiceField): 
        for (v, desc) in field.field.choices: 
            if v == val: 
                return desc 
    return val

def display_field_value(field):
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
