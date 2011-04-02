from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import TimestampModelMixin

class NotYetImplemented(Exception):
    pass


class Operator(TimestampModelMixin):
    display_name = models.CharField(max_length=255)
    query_string_partial = models.CharField(max_length=255)
    use_filter = models.BooleanField(default=True) # if False, use exclude
    order = models.IntegerField(default=100)

    class Meta(object):
        ordering = ("order",)

    def __unicode__(self):
        return "%s" % self.display_name

class RightSideType(TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name

    def prepare_query_value(self, value_to_prep):
        """Converts value (a string) into the appropriate type to query against"""
        if self.name == "text":
            return "'%s'" % value_to_prep
        else:
            raise NotYetImplemented


class RightSideValue(TimestampModelMixin):
    right_side_type = models.ForeignKey(RightSideType)
    value = models.TextField(blank=True, null=True)


    def __unicode__(self):
        return "%s: %s" % (self.right_side_type, self.value)

    @property
    def cleaned_query_value(self):
        """Converts value (a string) into the appropriate type to query against"""
        # raise NotYetImplemented

        # Idea/pseudocode
        if self.value:
            return self.right_side_type.prepare_query_value(self.value)
        else:
            return None

class LeftSide(TimestampModelMixin):
    display_name = models.CharField(max_length=255)
    query_string_partial = models.TextField()
    allowed_operators = models.ManyToManyField(Operator)
    allowed_right_side_types = models.ManyToManyField(RightSideType)
    order = models.IntegerField(default=100)

    def __unicode__(self):
        return "%s" % self.display_name
    
    class Meta(object):
        ordering = ("order",)

    @property
    def operators(self):
        return self.allowed_operators.all()
    
    @property
    def right_side_types(self):
        return self.allowed_right_side_types.all()

class Rule(TimestampModelMixin):
    left_side = models.ForeignKey(LeftSide, blank=True, null=True)
    operator = models.ForeignKey(Operator, blank=True, null=True)
    right_side_value = models.ForeignKey(RightSideValue, blank=True, null=True)

    target_model = None


    def __unicode__(self):
        return "Rule: %s %s %s" % (self.left_side, self.operator, self.right_side_value)

    @property
    def is_valid(self):
        """Boolean - if true, this rule is complete, and ok to query against."""
        raise NotYetImplemented
        return self.left_side and self.operator and self.right_side_value

    @property
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
        filter_str = "%s%s%s" % (self.left_side.query_string_partial, self.operator.query_string_partial, self.right_side_value.cleaned_query_value)
        if self.operator.use_filter:
            return "filter(%s)" % filter_str
        else:
            return "exclude(%s)" % filter_str


    @property
    def queryset(self):
        """Returns a working queryset of self.target_model's class, filtered/excluded 
           as appropriate"""
        if not self.target_model:
            raise Exception, "No target model defined!"
        else:
            return eval("self.target_model.objects.%s" % self.queryset_filter_string)

    class Meta(object):
        abstract = True
