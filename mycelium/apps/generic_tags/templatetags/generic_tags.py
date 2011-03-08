from django import template
from django.conf import settings
register = template.Library()
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

@register.inclusion_tag('generic_tags/_tags_and_add_tag.html')
def render_tags_and_add_tag(obj, namespace_string="", app_name="", tag_field="tags"):
    MEDIA_URL = settings.MEDIA_URL
    add_tag_url = reverse("%s:add_tag" % app_name)
    delete_tag_url = reverse("%s:remove_tag" % app_name, args=(obj.pk,))    
    search_results_url = reverse("%s:new_tag_search_results" % app_name)
    return locals()


@register.inclusion_tag('generic_tags/_js.html')
def generic_tags_js():
    MEDIA_URL = settings.MEDIA_URL
    return locals()
