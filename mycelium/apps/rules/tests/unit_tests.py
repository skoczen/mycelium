from test_factory import Factory
from nose.tools import istest
from rules.models import LeftSide, Operator, RightSideType, RightSideValue, Rule
from rules.tasks import populate_rule_components
from groups.models import GroupRule
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from django.db.models import Q

class TestRuleModelFunctions(DatabaseTestCase):
    def setUp(self):
        populate_rule_components()

    def test_left_side_operators_function(self):
        left_side = LeftSide.objects.get(display_name="has a general tag that")
        self.assertEqual(left_side.operators, left_side.allowed_operators.all())

    def test_left_side_right_side_type_function(self):
        left_side = LeftSide.objects.get(display_name="has a general tag that")
        self.assertEqual(left_side.right_side_types, left_side.allowed_right_side_types.all())


class TestPopulateRuleComponents(DatabaseTestCase):
    def setUp(self):
        populate_rule_components()


    def test_general_tags(self):
        # General tags are a valid left side, with operators exactly and contains, 
        # right hand side text

        left_side = LeftSide.objects.get(display_name="has a general tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__tags__name")
        self.assertEqual(left_side.display_name,  "has a general tag that")
        self.assertEqual(left_side.operators,  Operator.objects.filter(Q(display_name="is exactly") | Q(display_name="is not exactly") | Q(display_name="contains") | Q(display_name="does not contain") ) )
        self.assertEqual(left_side.right_side_types,  RightSideType.objects.filter(name="text"))
    
    def test_donor_tags(self):
        assert True == "Test written"
    
    def test_volunteer_tags(self):
        assert True == "Test written"
    
    def test_custom_tag_1(self):
        assert True == "Test written"

    def test_volunteer_status(self):
        assert True == "Test written"
    
    def test_last_donation(self):
        assert True == "Test written"

    def test_total_donation_amount_in_past_12_month(self):
        assert True == "Test written"
    
    def test_last_volunteer_shift(self):
        assert True == "Test written"
    
    def test_total_volunteer_hours_in_past_12_month(self):
        assert True == "Test written"

    def test_right_side_for_text(self):
        assert True == "Test written"

    def test_right_side_for_date(self):
        assert True == "Test written"

    def test_operator_display_name_and_query_string_model_for_is_exactly(self):
        assert True == "Test written"

    def test_operator_display_name_and_query_string_model_for_is_not_exactly(self):
        assert True == "Test written"

    def test_operator_display_name_and_query_string_model_for_contains(self):
        assert True == "Test written"

    def test_operator_display_name_and_query_string_model_for_does_not_contain(self):
        assert True == "Test written"
    
    def test_operator_display_name_and_query_string_model_for_is_on(self):
        assert True == "Test written"

    def test_operator_display_name_and_query_string_model_for_is_before(self):
        assert True == "Test written"

    def test_operator_display_name_and_query_string_model_for_is_after(self):
        assert True == "Test written"


    def test_operator_display_name_and_query_string_model_for_is_equal(self):
        assert True == "Test written"

    def test_operator_display_name_and_query_string_model_for_is_less_than(self):
        assert True == "Test written"

    def test_operator_display_name_and_query_string_model_for_is_more_than(self):
        assert True == "Test written"

    
    def test_left_side_ordering(self):
        assert True == "Test written"

    def test_operator_ordering(self):
        assert True == "Test written"    

    def test_populate_cleans_up_unused_rules(self):
        # create a custom tag
        # repopulate
        # make sure it's there
        # delete it
        # repopulate
        # make sure it's gone
        assert True == "Test written"

class TestQueryStringGeneration(DestructiveDatabaseTestCase):
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
