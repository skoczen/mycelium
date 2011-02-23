from django import template
from django.conf import settings
register = template.Library()
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.template.defaultfilters import date, timesince
import datetime



@register.filter
def shorttime(str):
    """Shorten a timesince entry, to lop off a second unit of time."""
    last_comma = str.find(",")
    if last_comma == -1:
        return str
    else:
        return str[:last_comma]

@register.filter
def reasonabletime(time,time_units=False):
    """Take a time in hours, and return a nice string."""
    # print "time_units: %s" % (time_units)

    if time_units == False:
        if time < 1:
            timeval = int(time*60)
            plural_string = ""
            if timeval != 1:
                plural_string = _("s")
            return "%s %s%s" % (timeval, _("minute"), plural_string)
        elif time < 24:
            timeval = int(time)
            plural_string = ""
            if timeval != 1:
                plural_string = _("s")
            return "%s %s%s" % (timeval, _("hour"), plural_string)
        elif time < 24*7:
            timeval = int(time/24)
            plural_string = ""
            if timeval != 1:
                plural_string = _("s")
            return "%s %s%s" % (timeval, _("day"), plural_string)
        elif time < 24*7*365:
            timeval = int(time/(24*7))
            plural_string = ""
            if timeval != 1:
                plural_string = _("s")
            return "%s %s%s" % (timeval, _("week"), plural_string)
        else:
            timeval = int(time/(24*7*365))
            plural_string = ""
            if timeval != 1:
                plural_string = _("s")
            return "%s %s%s" % (timeval, _("year"), plural_string)
    elif time_units == None:
        # default to hours
        return "%s %s" % (round(time), _("hours"))

    else:
        # handle what we're given
        timeval = int(time)
        plural_string = ""
        if timeval != 1:
            plural_string = _("s")
        if time_units == 1:
            return "%s %s%s" % (int(time), _("minute"), plural_string)
        elif time_units == 2:
            return "%s %s%s" % (int(time), _("hour"), plural_string)
        elif time_units == 3:
            return "%s %s%s" % (int(time), _("day"), plural_string)
        elif time_units == 4:
            return "%s %s%s" % (int(time), _("week"), plural_string)
        elif time_units == 5:
            return "%s %s%s" % (int(time), _("year"), plural_string)


@register.filter
def pretty_timesince(this_date):
    try:
        if datetime.datetime.now() - this_date < datetime.timedelta(minutes=1):
            return _("a few seconds ago")
        if this_date > datetime.datetime.now() - datetime.timedelta(days=14):
            return shorttime(timesince(this_date)) + _(" ago")
        else:
            return date(this_date)
    except:
        from qi_toolkit.helpers import print_exception
        print_exception()
        return date(this_date)
