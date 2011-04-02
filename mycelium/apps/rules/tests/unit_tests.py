from test_factory import Factory
from nose.tools import istest
from rules.models import LeftSide, Operator, RightSideType, RightSideValue, Rule
from rules.tasks import populate_rule_components
from groups.models import GroupRule
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.db.models import Q
from django.test import TestCase

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
    def _text_right_side_types(self):
        return RightSideType.objects.filter(name="text")
    
    @property
    def _date_right_side_types(self):
        return RightSideType.objects.filter(name="date")

    @property
    def _number_right_side_types(self):
        return RightSideType.objects.filter(name="number")


class TestRuleModelFunctions(QiUnitTestMixin, TestCase):
    fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        populate_rule_components()
        self.left_side = LeftSide.objects.get(display_name="has a general tag that")

    def test_left_side_operators_function(self):
        self.assertEqualQuerySets(self.left_side.operators,self.left_side.allowed_operators.all())

    def test_left_side_right_side_type_function(self):
        self.assertEqualQuerySets(self.left_side.right_side_types, self.left_side.allowed_right_side_types.all())


class TestPopulateRuleComponents(QiUnitTestMixin, RuleTestAbstractions, TestCase):
    fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        populate_rule_components()
    
    def test_any_tags(self):
        left_side = LeftSide.objects.get(display_name="have any tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__tags__name")
        self.assertEqualQuerySets(left_side.operators,  self._text_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._text_right_side_types  )

    def test_general_tags(self):
        left_side = LeftSide.objects.get(display_name="have a General tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__tagset__name='General',tagsetmembership__tags__name")
        self.assertEqualQuerySets(left_side.operators,  self._text_operators )
        self.assertEqualQuerySets(left_side.right_side_types,  self._text_right_side_types)
    
    def test_donor_tags(self):
        left_side = LeftSide.objects.get(display_name="have a Donor tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__tagset__name='Donor',tagsetmembership__tags__name")
        self.assertEqualQuerySets(left_side.operators,  self._text_operators )
        self.assertEqualQuerySets(left_side.right_side_types,  self._text_right_side_types)
    
    def test_volunteer_tags(self):
        left_side = LeftSide.objects.get(display_name="have a Volunteer tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__tagset__name='Volunteer',tagsetmembership__tags__name")
        self.assertEqualQuerySets(left_side.operators,  self._text_operators )
        self.assertEqualQuerySets(left_side.right_side_types,  self._text_right_side_types)
    
    def test_custom_tag_1(self):
        # make a new tagset
        from generic_tags.models import TagSet
        TagSet.objects.create(name="new test tagset")
        populate_rule_components()
        left_side = LeftSide.objects.get(display_name="have a new test tagset tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__tagset__name='new test tagset',tagsetmembership__tags__name")
        self.assertEqualQuerySets(left_side.operators,  self._text_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._text_right_side_types)

    def test_volunteer_status(self):
        left_side = LeftSide.objects.get(display_name="volunteer status")
        self.assertEqual(left_side.query_string_partial, "volunteer__status")
        self.assertEqualQuerySets(left_side.operators,  self._text_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._text_right_side_types)
    
    def test_last_donation(self):
        left_side = LeftSide.objects.get(display_name="last donation")
        self.assertEqual(left_side.query_string_partial, "donor__donation__date")
        self.assertEqualQuerySets(left_side.operators,  self._date_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._date_right_side_types)

    def test_total_donation_amount_in_past_12_month(self):
        left_side = LeftSide.objects.get(display_name="total donations in the last 12 months")
        self.assertEqual(left_side.query_string_partial, "donor__twelvemonth_total")
        self.assertEqualQuerySets(left_side.operators,  self._number_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._number_right_side_types)

    def test_last_volunteer_shift(self):
        left_side = LeftSide.objects.get(display_name="last volunteer shift")
        self.assertEqual(left_side.query_string_partial, "volunteer__completedshift__date")
        self.assertEqualQuerySets(left_side.operators,  self._date_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._date_right_side_types)

    def test_total_volunteer_hours_in_past_12_month(self):
        left_side = LeftSide.objects.get(display_name="total volunteer hours in the last 12 months")
        self.assertEqual(left_side.query_string_partial, "volunteer__twelvemonth_total")
        self.assertEqualQuerySets(left_side.operators,  self._number_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._number_right_side_types)

    def test_right_side_for_text(self):
        rs = self._text_right_side_types
        rs.count() == 1
        assert rs[0].name == "text"

    def test_right_side_for_date(self):
        rs = self._date_right_side_types
        rs.count() == 1
        assert rs[0].name == "date"
    
    def test_right_side_for_number(self):
        rs = self._number_right_side_types
        rs.count() == 1
        assert rs[0].name == "number"

    def test_operator_display_name_and_query_string_model_for_is_exactly(self):
        o = Operator.objects.get(display_name="is exactly")
        self.assertEqual(o.query_string_partial, "__iexact")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_not_exactly(self):
        o = Operator.objects.get(display_name="is not exactly")
        self.assertEqual(o.query_string_partial, "__iexact")
        self.assertEqual(o.use_filter, False)

    def test_operator_display_name_and_query_string_model_for_contains(self):
        o = Operator.objects.get(display_name="contains")
        self.assertEqual(o.query_string_partial, "__icontains")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_does_not_contain(self):
        o = Operator.objects.get(display_name="does not contain")
        self.assertEqual(o.query_string_partial, "__icontains")
        self.assertEqual(o.use_filter, False)
    
    def test_operator_display_name_and_query_string_model_for_is_on(self):
        o = Operator.objects.get(display_name="is on")
        self.assertEqual(o.query_string_partial, "=")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_before(self):
        o = Operator.objects.get(display_name="is before")
        self.assertEqual(o.query_string_partial, "__lt")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_after(self):
        o = Operator.objects.get(display_name="is after")
        self.assertEqual(o.query_string_partial, "__gt")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_equal(self):
        o = Operator.objects.get(display_name="is equal to")
        self.assertEqual(o.query_string_partial, "=")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_less_than(self):
        o = Operator.objects.get(display_name="is less than")
        self.assertEqual(o.query_string_partial, "__lt")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_more_than(self):
        o = Operator.objects.get(display_name="is more than")
        self.assertEqual(o.query_string_partial, "__gt")
        self.assertEqual(o.use_filter, True)

    def test_left_side_ordering(self):
        list_of_names = [l.display_name for l in LeftSide.objects.all()]
        target_list_of_names = [
            "have any tag that",
            "have a General tag that",
            "have a Volunteer tag that",
            "have a Donor tag that",
            "volunteer status",
            "last donation",
            "total donations in the last 12 months",
            "last volunteer shift",
            "total volunteer hours in the last 12 months"
        ]
        self.assertEqual(list_of_names,target_list_of_names)

    def test_operator_ordering(self):
        list_of_names = [o.display_name for o in Operator.objects.all()]
        target_list_of_names = [
            "is exactly",
            "is not exactly",
            "contains",
            "does not contain",
            "is on",
            "is before",
            "is after",
            "is equal to",
            "is less than",
            "is more than",
        ]
        self.assertEqual(list_of_names,target_list_of_names)

    def test_populate_cleans_up_unused_rules(self):
        # create a custom tag
        from generic_tags.models import TagSet
        ts1 = TagSet.objects.create(name="new test tagset")
        
        # repopulate
        populate_rule_components()
        
        # make sure it's there
        left_side = LeftSide.objects.get(display_name="have a new test tagset tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__tagset__name='new test tagset',tagsetmembership__tags__name")
        self.assertEqualQuerySets(left_side.operators,  self._text_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._text_right_side_types)

        # delete it
        ts1.delete()

        # repopulate
        populate_rule_components()
        
        # make sure it's gone
        self.assertEqual(LeftSide.objects.filter(display_name="have a new test tagset tag that").count(), 0)

class TestQueryStringGeneration(DestructiveDatabaseTestCase, QiUnitTestMixin):
    def setUp(self):
        populate_rule_components()

### RIGHT SIDE QUERY VALUE ###
    def test_right_side_value_query_value_works_for_text(self):
        assert True == "Test written"

    def test_right_side_value_query_value_works_for_date(self):
        assert True == "Test written"

    def test_right_side_type_query_value_works_for_text(self):
        assert True == "Test written"

    def test_right_side_type_query_value_works_for_date(self):
        assert True == "Test written"
    

### NEW GROUP CREATES THE RIGHT RECORDS ###
    def test_create_new_group_rule_for_general_tag_contains(self):
        # create a new group rule
        # assert the correct models exist
        assert True == "Test written"

    def test_create_new_group_rule_for_custom_tag_is_not_exactly(self):
        # create a new group rule
        # assert the correct models exist
        assert True == "Test written"
    
    def test_create_new_group_rule_for_last_volunteer_shift_is_on(self):
        # create a new group rule
        # assert the correct models exist
        assert True == "Test written"

    def test_create_new_group_rule_for_last_donation_is_after(self):
        # create a new group rule
        # assert the correct models exist
        assert True == "Test written"

    def test_create_new_group_rule_for_volunteer_status_is_active(self):
        # create a new group rule
        # assert the correct models exist
        assert True == "Test written"

    def test_create_new_group_rule_for_volunteer_status_is_inactive(self):
        # create a new group rule
        # assert the correct models exist
        assert True == "Test written"

### GROUPS RETURN THE RIGHT QUERYSETS ###
    def test_queryset_for_new_group_rule_for_general_tag_contains(self):
        assert True == "Test written"
        # hand-create a few people, some of whom match, and others who don't
        # create a new group rule
        self.test_create_new_group_rule_for_general_tag_contains()
        # assert the queryset string is right
        # get the queryset, make sure it matches a hand-created one.

    def test_queryset_for_new_group_rule_for_custom_tag_is_not_exactly(self):
        assert True == "Test written"
        # hand-create a few people, some of whom match, and others who don't
        # create a new group rule
        self.test_create_new_group_rule_for_custom_tag_is_not_exactly()
        # assert the queryset string is right
        # get the queryset, make sure it matches a hand-created one.
    
    def test_queryset_for_new_group_rule_for_last_volunteer_shift_is_on(self):
        assert True == "Test written"
        # hand-create a few people, some of whom match, and others who don't
        # create a new group rule
        self.test_create_new_group_rule_for_last_volunteer_shift_is_on()
        # assert the queryset string is right
        # get the queryset, make sure it matches a hand-created one.

    def test_queryset_for_new_group_rule_for_last_donation_is_after(self):
        assert True == "Test written"
        # hand-create a few people, some of whom match, and others who don't
        # create a new group rule
        self.test_create_new_group_rule_for_last_donation_is_after()
        # assert the queryset string is right
        # get the queryset, make sure it matches a hand-created one.


    def test_queryset_for_new_group_rule_for_volunteer_status_is_active(self):
        # hand-create a few people, some of whom match, and others who don't. Include temporarily inactive
        # create a new group rule
        self.test_create_new_group_rule_for_volunteer_status_is_active()
        # assert the queryset string is right
        # get the queryset, make sure it matches a hand-created one.


    def test_queryset_for_new_group_rule_for_volunteer_status_is_inactive(self):
        # hand-create a few people, some of whom match, and others who don't. Include temporarily inactive
        # create a new group rule
        self.test_create_new_group_rule_for_volunteer_status_is_inactive()
        # assert the queryset string is right
        # get the queryset, make sure it matches a hand-created one.
