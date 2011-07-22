from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import TimestampModelMixin
from django.db.models import Q
import datetime
from dateutil import parser
from picklefield.fields import PickledObjectField
from rules import NotYetImplemented, IncompleteRuleException
from generic_tags.models import Tag

from accounts.models import AccountBasedModel

class Operator(AccountBasedModel, TimestampModelMixin):
    display_name = models.CharField(max_length=255)
    query_string_partial = models.CharField(max_length=255)
    use_filter = models.BooleanField(default=True) # if False, use exclude
    order = models.IntegerField(default=100)

    class Meta(object):
        ordering = ("order",)

    def __unicode__(self):
        return "%s" % self.display_name

class RightSideType(AccountBasedModel, TimestampModelMixin):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name

    def prepare_query_value(self, value_to_prep):
        """Converts value (a string) into the appropriate type to query against"""
        if self.name == "text":
            return "'%s'" % value_to_prep
        if self.name == "date":
            d = parser.parse(value_to_prep).date()
            return "datetime.date(month=%s,day=%s,year=%s)" % (d.month, d.day, d.year)
        if self.name == "choices":
            return "'%s'" % value_to_prep
        if self.name == "number":
            return "'%s'" % int(value_to_prep)
        else:
            raise NotYetImplemented



class LeftSide(AccountBasedModel, TimestampModelMixin):
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
    
    @property
    def first_right_side_type(self):
        return self.allowed_right_side_types.all()[0]
    
    @property
    def is_date(self):
        return self.first_right_side_type.name == "date"

class Rule(TimestampModelMixin):
    left_side = models.ForeignKey(LeftSide, blank=True, null=True)
    operator = models.ForeignKey(Operator, blank=True, null=True)
    right_side_type = models.ForeignKey(RightSideType, blank=True, null=True)
    right_side_value = models.TextField(blank=True, null=True)

    target_model = None


    def __unicode__(self):
        return "Rule: %s %s %s" % (self.left_side, self.operator, self.right_side_value)

    class Meta(object):
        abstract = True

    @property
    def is_valid(self):
        """Boolean - if true, this rule is complete, and ok to query against."""
        return self.left_side_id and self.operator_id and self.right_side_value and self.right_side_type_id
    
    @property
    def is_blank(self):
        return not self.left_side_id and not self.operator_id and not self.right_side_value and not self.right_side_type_id

    @property
    def cleaned_right_side_value(self):
        return self.right_side_type.prepare_query_value(self.right_side_value)

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
            return ""
        else:
            filter_str = "%s%s%s" % (self.left_side.query_string_partial, self.operator.query_string_partial, self.cleaned_right_side_value)
            if self.left_side.add_closing_paren:
                filter_str = "%s)" % filter_str
            
            if self.operator.use_filter:
                filter_str =  "filter(%s)" % filter_str
            else:
                filter_str = "exclude(%s)" % filter_str
            
            return filter_str

    # @property
    # def queryset(self):
    #     """Returns a working queryset of self.target_model's class, filtered/excluded 
    #        as appropriate"""
    #     if not self.target_model:
    #         raise IncompleteRuleException, "No target model defined!"
    #     else:
    #         return eval("self.target_model.objects.%s" % self.queryset_filter_string)

    # def queryset_callable(self):
    #     return self.queryset


class RuleGroup(models.Model):
    rules_boolean = models.BooleanField(default=True) # True==All  False==Any

    class Meta(object):
        abstract = True

    @property
    def rules(self):
        return self.rule_set.all()
    
    @property
    def has_a_valid_rule(self):
        for r in self.rules:
            if r.is_valid:
                return True
        return False

    @property
    def num_blank_rules(self):
        return self.rules.filter(left_side=None, operator=None, right_side_type=None, right_side_value=None).count()
    
    def make_blank_rule(self):
        return self.rules_set.create()

    @property
    def members(self, request=None):
        # TODO: cache/improve the speed.
        if hasattr(self.target_model,"raw_objects"):
            objects_str = "objects_by_account(self.account)"
        else:
            objects_str = "objects"

        results = ""
        if self.has_a_valid_rule:
            if self.rules_boolean:
                results = "self.target_model.%s.all()" % objects_str
                for r in self.rules:
                    if r.is_valid:
                        results = "%s.%s" % (results, r.queryset_filter_string)
            else:
                results = "self.target_model.%s.none()" % objects_str
                for r in self.rules:
                    if r.is_valid:
                        results = "%s | %s%s.%s " % (results, "self.target_model.", objects_str,  r.queryset_filter_string)
        else:
            return eval("self.target_model.%s.none()" % objects_str )

        qs = eval(results).distinct().all()

        return qs
        

