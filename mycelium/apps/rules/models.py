from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import TimestampModelMixin

class NotYetImplemented(Exception):
    pass


class Operator(TimestampModelMixin):
    display_name = models.CharField(max_length=255)
    query_string_partial = models.CharField(max_length=255)
    order = models.IntegerField(default=100)


class RightSideType(TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True)

    def prepare_query_value(self, value_to_prep):
        """Converts value (a string) into the appropriate type to query against"""
        raise NotYetImplemented


class RightSideValue(TimestampModelMixin):
    right_side_type = models.ForeignKey(RightSideType)
    value = models.TextField(blank=True, null=True)

    def cleaned_query_value(self):
        """Converts value (a string) into the appropriate type to query against"""
        raise NotYetImplemented

        # Idea/pseudocode
        if self.right_side_value:
            return self.right_side_type.prepare_query_value(self.value)
        else:
            return None

class LeftSide(TimestampModelMixin):
    display_name = models.CharField(max_length=255)
    query_string_partial = models.TextField()
    allowed_operators = models.ManyToManyField(Operator)
    allowed_right_side_types = models.ManyToManyField(RightSideType)


class Rule(TimestampModelMixin):
    left_side = models.ForeignKey(LeftSide, blank=True, null=True)
    operator = models.ForeignKey(Operator, blank=True, null=True)
    right_side_value = models.ForeignKey(RightSideValue, blank=True, null=True)

    target_model = None

    @property
    def is_valid(self):
        """Boolean - if true, this rule is complete, and ok to query against."""
        return self.left_side and self.operator and self.right_side_value


    def queryset_filter_string(self):
        """Creates a filter/exclude string, with string replace placeholders for:
            operator - to be filled in by the operator's query_string_partial
            right_side_value - to be filled in by the right_side_value's cleaned_query_value
        
            example - searching for people named joe:
            eg:  "%(operator)s%(right_side_value)s" % {
                                                            "operator": "__icontains=",
                                                            "right_side_value": "joe",
                                                        }
        """
        raise NotYetImplemented


    def queryset(self):
        """Returns a working queryset of self.target_model's class, filtered/excluded 
           as appropriate"""
        raise NotYetImplemented

    class Meta(object):
        abstract = True
