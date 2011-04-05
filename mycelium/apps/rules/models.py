from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import TimestampModelMixin
from django.db.models import Q
from generic_tags.models import TagSetMembership
import datetime
from dateutil.parser import parse
from picklefield.fields import PickledObjectField
from rules import NotYetImplemented, IncompleteRuleException


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
        if self.name == "date":
            d = parse(value_to_prep).date()
            return "datetime.date(month=%s,day=%s,year=%s)" % (d.month, d.day, d.year)
        if self.name == "choices":
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
        if self.value:
            return self.right_side_type.prepare_query_value(self.value)
        else:
            raise Exception, "No Value"

class LeftSide(TimestampModelMixin):
    display_name = models.CharField(max_length=255)
    query_string_partial = models.TextField()
    allowed_operators = models.ManyToManyField(Operator)
    allowed_right_side_types = models.ManyToManyField(RightSideType)
    order = models.IntegerField(default=100)
    add_closing_paren = models.BooleanField(default=False)
    choices = PickledObjectField(blank=True, null=True)

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

    class Meta(object):
        abstract = True


    @property
    def is_valid(self):
        """Boolean - if true, this rule is complete, and ok to query against."""
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
        if not self.is_valid:
            raise IncompleteRuleException
        else:
            filter_str = "%s%s%s" % (self.left_side.query_string_partial, self.operator.query_string_partial, self.right_side_value.cleaned_query_value)
            if self.left_side.add_closing_paren:
                filter_str = "%s)" % filter_str
            
            if self.operator.use_filter:
                return "filter(%s)" % filter_str
            else:
                return "exclude(%s)" % filter_str


    @property
    def queryset(self):
        """Returns a working queryset of self.target_model's class, filtered/excluded 
           as appropriate"""
        if not self.target_model:
            raise IncompleteRuleException, "No target model defined!"
        else:
            return eval("self.target_model.objects.%s" % self.queryset_filter_string)

    def queryset_callable(self):
        return self.queryset


class RuleGroup(models.Model):
    rules_boolean = models.BooleanField(default=True) # True==All  False==Any

    class Meta(object):
        abstract = True

    @property
    def rules(self):
        return self.rule_set.all()

    @property
    def members(self):
        # TODO: cache/improve the speed.

        results = ""
        if self.rules_boolean:
            results = "self.target_model.objects.all()"
            for r in self.rules:
                results = "%s.%s" % (results, r.queryset_filter_string)
        else:
            for r in self.rules:
                results = "self.target_model.objects.none()"
                results = "%s | %s.%s " (results, "self.target_model.objects.", r.queryset_filter_string)
        
        return eval(results)


