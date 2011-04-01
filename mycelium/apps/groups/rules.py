class Rule(object):
    left_side_display = ""
    left_side_qs = ""
    operator = ""
    right_side = ""

    left_side_available_operators = ""
"""
operators:

is_exactly          filter(__iequals)
is_not_exactly      exclude(__iequals)
contains            filter(__icontains)
does not contain    exclude(__icontains)
is on               date=
is before           date__lt=
is after            date__gt


RULE_LEFT_SIDES = [
    ()
]

"""