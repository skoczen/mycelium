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
    right_type_text     = RightSideType.objects.get_or_create(name="text")[0]
    right_type_date     = RightSideType.objects.get_or_create(name="date")[0]
    right_type_number   = RightSideType.objects.get_or_create(name="number")[0]
    right_type_choices   = RightSideType.objects.get_or_create(name="choices")[0]
    all_right_side_types = [right_type_text, right_type_date, right_type_number, right_type_choices]

    # Operators
    all_operators = []
    operator_is =                   Operator.objects.get_or_create(display_name="is"                , query_string_partial="="             , use_filter=True)[0]
    operator_is_not =               Operator.objects.get_or_create(display_name="is not"            , query_string_partial="="             , use_filter=False)[0]
    operator_is_exactly =           Operator.objects.get_or_create(display_name="is exactly"        , query_string_partial="__iexact="     , use_filter=True)[0]
    operator_is_not_exactly =       Operator.objects.get_or_create(display_name="is not exactly"    , query_string_partial="__iexact="     , use_filter=False)[0]
    operator_contains =             Operator.objects.get_or_create(display_name="contains"          , query_string_partial="__icontains="  , use_filter=True)[0]
    operator_does_not_contain =     Operator.objects.get_or_create(display_name="does not contain"  , query_string_partial="__icontains="  , use_filter=False)[0]
    operator_is_on =                Operator.objects.get_or_create(display_name="is on"             , query_string_partial="="             , use_filter=True)[0]
    operator_is_before =            Operator.objects.get_or_create(display_name="is before"         , query_string_partial="__lt="         , use_filter=True)[0]
    operator_is_after =             Operator.objects.get_or_create(display_name="is after"          , query_string_partial="__gt="         , use_filter=True)[0]
    operator_is_equal =             Operator.objects.get_or_create(display_name="is equal to"       , query_string_partial="="             , use_filter=True)[0]
    operator_is_less_than =         Operator.objects.get_or_create(display_name="is less than"      , query_string_partial="__lt="         , use_filter=True)[0]
    operator_is_more_than =         Operator.objects.get_or_create(display_name="is more than"      , query_string_partial="__gt="         , use_filter=True)[0]
    all_operators = [   operator_is_exactly, operator_is_not_exactly, operator_contains, operator_does_not_contain, 
                        operator_is_on, operator_is_before, operator_is_after,
                        operator_is_equal, operator_is_less_than, operator_is_more_than,
                        operator_is, operator_is_not
                    ]

    # Helper methods
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

    def _add_date_operators(ls):
        ls.allowed_operators.add(operator_is_on)
        ls.allowed_operators.add(operator_is_before)
        ls.allowed_operators.add(operator_is_after)
        ls.save()
    
    def _add_right_type_date(ls):
        ls.allowed_right_side_types.add(right_type_date)
        ls.save()
    
    def _add_operators_and_right_side_date(ls):
        _add_date_operators(ls)
        _add_right_type_date(ls)

    def _add_number_operators(ls):
        ls.allowed_operators.add(operator_is_equal)
        ls.allowed_operators.add(operator_is_less_than)
        ls.allowed_operators.add(operator_is_more_than)
        ls.save()
    
    def _add_right_type_number(ls):
        ls.allowed_right_side_types.add(right_type_number)
        ls.save()
    
    def _add_operators_and_right_side_number(ls):
        _add_number_operators(ls)
        _add_right_type_number(ls)

    def _add_tag_operators(ls):
        ls.allowed_operators.add(operator_is_exactly)
        ls.allowed_operators.add(operator_contains)
        ls.save()    

    def _add_operators_and_right_side_tag(ls):
        _add_tag_operators(ls)
        _add_right_type_text(ls)

    def _add_choices_operators(ls):
        ls.allowed_operators.add(operator_is)
        ls.allowed_operators.add(operator_is_not)
        ls.save()
    
    def _add_right_type_choices(ls):
        ls.allowed_right_side_types.add(right_type_choices)
        ls.save()
    
    def _add_operators_and_right_side_choices(ls):
        _add_choices_operators(ls)
        _add_right_type_choices(ls)


    def _add_to_all_left_sides(ls):
        all_left_sides.append(ls)

    def left_side_for_text(**kwargs):
        if not "display_name" in kwargs or not "query_string_partial" in kwargs:
            raise Exception, "display_name and query_string_partial not passed!"

        ls = LeftSide.objects.get_or_create(**kwargs)[0]
        _add_operators_and_right_side_text(ls)
        _add_to_all_left_sides(ls)
        return ls

    def left_side_for_date(**kwargs):
        if not "display_name" in kwargs or not "query_string_partial" in kwargs:
            raise Exception, "display_name and query_string_partial not passed!"

        ls = LeftSide.objects.get_or_create(**kwargs)[0]
        _add_operators_and_right_side_date(ls)
        _add_to_all_left_sides(ls)
        return ls

    def left_side_for_number(**kwargs):
        if not "display_name" in kwargs or not "query_string_partial" in kwargs:
            raise Exception, "display_name and query_string_partial not passed!"

        ls = LeftSide.objects.get_or_create(**kwargs)[0]
        _add_operators_and_right_side_number(ls)
        _add_to_all_left_sides(ls)
        return ls
    
    def left_side_for_tag(**kwargs):
        if not "display_name" in kwargs or not "query_string_partial" in kwargs:
            raise Exception, "display_name and query_string_partial not passed!"

        ls = LeftSide.objects.get_or_create(**kwargs)[0]
        _add_operators_and_right_side_tag(ls)
        _add_to_all_left_sides(ls)
        return ls

    def left_side_for_choices(**kwargs):
        if not "display_name" in kwargs or not "query_string_partial" in kwargs:
            raise Exception, "display_name and query_string_partial not passed!"

        ls = LeftSide.objects.get_or_create(**kwargs)[0]
        _add_operators_and_right_side_choices(ls)
        _add_to_all_left_sides(ls)
        return ls

    # dependencies
    from volunteers import VOLUNTEER_STATII

    # Left sides - built-ins
    left_side_for_tag (     display_name="have any tag that"                            ,query_string_partial="tagsetmembership__taggedtagsetmembership__tag__name" , order=10     , add_closing_paren=False)
    left_side_for_choices(  display_name="volunteer status"                             ,query_string_partial="volunteer__status"                                   , order=100    , choices=VOLUNTEER_STATII)
    left_side_for_date(     display_name="last donation"                                ,query_string_partial="donor__donation__date"                               , order=110     )
    # left_side_for_number(   display_name="total donations in the last 12 months"        ,query_string_partial="donor__twelvemonth_total"                            , order=120     )
    left_side_for_date(     display_name="last volunteer shift"                         ,query_string_partial="volunteer__completedshift__date"                     , order=130     )    
    # left_side_for_number(   display_name="total volunteer hours in the last 12 months"  ,query_string_partial="volunteer__twelvemonth_total"                        , order=140     )

    # Left sides - generateds
    from generic_tags.models import TagSet
    i = 0
    for ts in TagSet.objects.all():
        i = i+1
        left_side_for_tag(display_name="have a %s tag that" % (ts.name) ,
                            query_string_partial="tagsetmembership__in=TagSetMembership.objects.filter(tagset__name='%s',taggedtagsetmembership__tag__name" % (ts.name), 
                            order=20+i,
                            add_closing_paren=True)
                                                                                                


    # Cleanup
    for rs in RightSideType.objects.all():
        if rs not in all_right_side_types:
            rs.delete()
    
    for o in Operator.objects.all():
        if o not in all_operators:
            o.delete()
    
    for ls in LeftSide.objects.all():
        if ls not in all_left_sides:
            ls.delete()
    