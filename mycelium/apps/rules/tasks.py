from rules.models import LeftSide, Operator, RightSideType

def populate_rule_components(*args, **kwargs):
    """This function performs several actions, and is idempotent.

    In order, it:

    - Sets up built-in rule options (like volunteer status)
    - Sets up data-driven rule options (like custom tag sets)
    - Cleans up unused rule options

    """
    raise Exception, "Not Yet Implemented"

    # is_exactly          filter(__iexact)
    # is_not_exactly      exclude(__iexact)
    # contains            filter(__icontains)
    # does not contain    exclude(__icontains)
    # is on               date=
    # is before           date__lt=
    # is after            date__gt
    
    pass