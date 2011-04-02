from rules.models import LeftSide, Operator, RightSideType

def populate_rule_components(*args, **kwargs):
    """This function performs several actions, and is idempotent.

    In order, it:

    - Sets up built-in rule options (like volunteer status)
    - Sets up data-driven rule options (like custom tag sets)
    - Cleans up unused rule options

    """
    # RightSideTypes
    all_right_side_types = []
    right_type_text = RightSideType.objects.get_or_create(name="text")[0]
    right_type_date = RightSideType.objects.get_or_create(name="date")[0]
    all_right_side_types = [right_type_text, right_type_date]

    # Operators
    all_operators = []
    operator_is_exactly =           Operator.objects.get_or_create(display_name="is exactly"        , query_string_partial="__iexact"     , use_filter=True)[0]
    operator_is_not_exactly =       Operator.objects.get_or_create(display_name="is not exactly"    , query_string_partial="__iexact"     , use_filter=False)[0]
    operator_contains =             Operator.objects.get_or_create(display_name="contains"          , query_string_partial="__icontains"  , use_filter=True)[0]
    operator_does_not_contain =     Operator.objects.get_or_create(display_name="does not contain"  , query_string_partial="__icontains"  , use_filter=False)[0]
    operator_is_on =                Operator.objects.get_or_create(display_name="is on"             , query_string_partial="="            , use_filter=True)[0]
    operator_is_before =            Operator.objects.get_or_create(display_name="is before"         , query_string_partial="__lt"         , use_filter=True)[0]
    operator_is_after =             Operator.objects.get_or_create(display_name="is after"          , query_string_partial="__gt"         , use_filter=True)[0]
    # operator_is_equal =             Operator.objects.get_or_create(display_name="is equal"          , query_string_partial="="            , use_filter=True)[0]
    # operator_is_less_than =         Operator.objects.get_or_create(display_name="is less than"      , query_string_partial="__lt"         , use_filter=True)[0]
    # operator_is_more_than =         Operator.objects.get_or_create(display_name="is more than"      , query_string_partial="__gt"         , use_filter=True)[0]
    all_operators = [operator_is_exactly, operator_is_not_exactly, operator_contains, operator_does_not_contain, operator_is_on, operator_is_before, operator_is_after]


    all_left_sides = []
    def _add_text_operators(ls):
        ls.allowed_operators.add(operator_is_exactly)
        ls.allowed_operators.add(operator_is_not_exactly)
        ls.allowed_operators.add(operator_contains)
        ls.allowed_operators.add(operator_does_not_contain)
        ls.save()
    
    def _add_right_type_text(ls):
        ls.allowed_right_side_types.add(right_type_text)
        ls.save()
    
    def _add_operators_and_right_side_text(ls):
        _add_text_operators(ls)
        _add_right_type_text(ls)

    def _add_to_all_left_sides(ls):
        all_left_sides.append(ls)

    def left_side_for_text(display_name=None, query_string_partial=None):
        if not display_name or not query_string_partial:
            raise Exception, "display_name and query_string_partial not passed!"
        
        ls = LeftSide.objects.get_or_create(display_name=display_name,query_string_partial=query_string_partial)[0]
        _add_operators_and_right_side_text(ls)
        _add_to_all_left_sides(ls)
        return ls
   

    # Left sides - built-ins
    # ls_any_tag = 
    ls_general_tags =         left_side_for_text(display_name="has a general tag that",query_string_partial="tagsetmembership__tags__name")

