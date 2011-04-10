from rules.models import LeftSide, Operator, RightSideType, Rule
from django.db.models import Q

class RuleTestAbstractions(object):
    @property
    def _text_operators(self):
        return Operator.objects.filter(Q(display_name="is exactly") | Q(display_name="is not exactly") | Q(display_name="contains") | Q(display_name="does not contain") )

    @property
    def _date_operators(self):
        return Operator.objects.filter(Q(display_name="is on") | Q(display_name="is before") | Q(display_name="is after"))

    @property
    def _number_operators(self):
        return Operator.objects.filter(Q(display_name="is equal to") | Q(display_name="is less than") | Q(display_name="is more than"))

    @property
    def _tag_operators(self):
        return Operator.objects.filter(Q(display_name="is exactly") | Q(display_name="contains") )

    @property
    def _choices_operators(self):
        return Operator.objects.filter(Q(display_name="is") | Q(display_name="is not") )

    @property
    def _text_right_side_types(self):
        return RightSideType.objects.filter(name="text")
    
    @property
    def _date_right_side_types(self):
        return RightSideType.objects.filter(name="date")

    @property
    def _number_right_side_types(self):
        return RightSideType.objects.filter(name="number")

    @property
    def _choices_right_side_types(self):
        return RightSideType.objects.filter(name="choices")