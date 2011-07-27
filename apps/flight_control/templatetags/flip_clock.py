from django import template
register = template.Library()
from django.utils.translation import ugettext as _


@register.inclusion_tag('flip_clock/_flip_clock.html')
def flip_clock(number, caption=""):
    return locals()
