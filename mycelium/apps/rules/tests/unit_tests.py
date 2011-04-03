from test_factory import Factory
from nose.tools import istest
from rules.models import LeftSide, Operator, RightSideType, RightSideValue, Rule
from rules.tasks import populate_rule_components
from groups.models import GroupRule
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.db.models import Q
from django.test import TestCase
from generic_tags.models import TagSet
from people.models import Person
import datetime

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


class TestRuleModelFunctions(QiUnitTestMixin, TestCase):
    fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        populate_rule_components()
        self.left_side = LeftSide.objects.get(display_name="have a general tag that")

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
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__taggedtagsetmembership__tag__name")
        self.assertEqualQuerySets(left_side.operators,  self._tag_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._text_right_side_types  )
        self.assertEqual(left_side.add_closing_paren, False)

    def test_general_tags(self):
        left_side = LeftSide.objects.get(display_name="have a General tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__in=TagSetMembership.objects.filter(tagset__name='General',taggedtagsetmembership__tag__name")
        self.assertEqualQuerySets(left_side.operators,  self._tag_operators )
        self.assertEqualQuerySets(left_side.right_side_types,  self._text_right_side_types)
        self.assertEqual(left_side.add_closing_paren, True)
    
    def test_donor_tags(self):
        left_side = LeftSide.objects.get(display_name="have a Donor tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__in=TagSetMembership.objects.filter(tagset__name='Donor',taggedtagsetmembership__tag__name")
        self.assertEqualQuerySets(left_side.operators,  self._tag_operators )
        self.assertEqualQuerySets(left_side.right_side_types,  self._text_right_side_types)
        self.assertEqual(left_side.add_closing_paren, True)
    
    def test_volunteer_tags(self):
        left_side = LeftSide.objects.get(display_name="have a Volunteer tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__in=TagSetMembership.objects.filter(tagset__name='Volunteer',taggedtagsetmembership__tag__name")
        self.assertEqualQuerySets(left_side.operators,  self._tag_operators )
        self.assertEqualQuerySets(left_side.right_side_types,  self._text_right_side_types)
        self.assertEqual(left_side.add_closing_paren, True)
    
    def test_custom_tag_1(self):
        # make a new tagset
        TagSet.objects.get_or_create(name="new test tagset")
        populate_rule_components()
        left_side = LeftSide.objects.get(display_name="have a new test tagset tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__in=TagSetMembership.objects.filter(tagset__name='new test tagset',taggedtagsetmembership__tag__name")
        self.assertEqualQuerySets(left_side.operators,  self._tag_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._text_right_side_types)
        self.assertEqual(left_side.add_closing_paren, True)

        return left_side

    def test_volunteer_status(self):
        left_side = LeftSide.objects.get(display_name="volunteer status")
        self.assertEqual(left_side.query_string_partial, "volunteer__status")
        self.assertEqualQuerySets(left_side.operators,  self._choices_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._choices_right_side_types)
        self.assertEqual(left_side.add_closing_paren, False)
    
    def test_last_donation(self):
        left_side = LeftSide.objects.get(display_name="last donation")
        self.assertEqual(left_side.query_string_partial, "donor__donation__date")
        self.assertEqualQuerySets(left_side.operators,  self._date_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._date_right_side_types)
        self.assertEqual(left_side.add_closing_paren, False)

    def test_total_donation_amount_in_past_12_month(self):
        left_side = LeftSide.objects.get(display_name="total donations in the last 12 months")
        self.assertEqual(left_side.query_string_partial, "donor__twelvemonth_total")
        self.assertEqualQuerySets(left_side.operators,  self._number_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._number_right_side_types)
        self.assertEqual(left_side.add_closing_paren, False)

    def test_last_volunteer_shift(self):
        left_side = LeftSide.objects.get(display_name="last volunteer shift")
        self.assertEqual(left_side.query_string_partial, "volunteer__completedshift__date")
        self.assertEqualQuerySets(left_side.operators,  self._date_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._date_right_side_types)
        self.assertEqual(left_side.add_closing_paren, False)

    def test_total_volunteer_hours_in_past_12_month(self):
        left_side = LeftSide.objects.get(display_name="total volunteer hours in the last 12 months")
        self.assertEqual(left_side.query_string_partial, "volunteer__twelvemonth_total")
        self.assertEqualQuerySets(left_side.operators,  self._number_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._number_right_side_types)
        self.assertEqual(left_side.add_closing_paren, False)

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

    def test_right_side_for_choices(self):
        rs = self._choices_right_side_types
        rs.count() == 1
        assert rs[0].name == "choices"


    def test_operator_display_name_and_query_string_model_for_is_exactly(self):
        o = Operator.objects.get(display_name="is exactly")
        self.assertEqual(o.query_string_partial, "__iexact=")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_not_exactly(self):
        o = Operator.objects.get(display_name="is not exactly")
        self.assertEqual(o.query_string_partial, "__iexact=")
        self.assertEqual(o.use_filter, False)

    def test_operator_display_name_and_query_string_model_for_contains(self):
        o = Operator.objects.get(display_name="contains")
        self.assertEqual(o.query_string_partial, "__icontains=")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_does_not_contain(self):
        o = Operator.objects.get(display_name="does not contain")
        self.assertEqual(o.query_string_partial, "__icontains=")
        self.assertEqual(o.use_filter, False)
    
    def test_operator_display_name_and_query_string_model_for_is_on(self):
        o = Operator.objects.get(display_name="is on")
        self.assertEqual(o.query_string_partial, "=")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_before(self):
        o = Operator.objects.get(display_name="is before")
        self.assertEqual(o.query_string_partial, "__lt=")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_after(self):
        o = Operator.objects.get(display_name="is after")
        self.assertEqual(o.query_string_partial, "__gt=")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_equal(self):
        o = Operator.objects.get(display_name="is equal to")
        self.assertEqual(o.query_string_partial, "=")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_less_than(self):
        o = Operator.objects.get(display_name="is less than")
        self.assertEqual(o.query_string_partial, "__lt=")
        self.assertEqual(o.use_filter, True)

    def test_operator_display_name_and_query_string_model_for_is_more_than(self):
        o = Operator.objects.get(display_name="is more than")
        self.assertEqual(o.query_string_partial, "__gt=")
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
            "is",
            "is not",
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
        ts1 = TagSet.objects.get_or_create(name="new test tagset")[0]
        
        # repopulate
        populate_rule_components()
        
        # make sure it's there
        left_side = LeftSide.objects.get(display_name="have a new test tagset tag that")
        self.assertEqual(left_side.query_string_partial, "tagsetmembership__in=TagSetMembership.objects.filter(tagset__name='new test tagset',taggedtagsetmembership__tag__name")
        self.assertEqualQuerySets(left_side.operators,  self._tag_operators )
        self.assertEqualQuerySets(left_side.right_side_types, self._text_right_side_types)

        # delete it
        ts1.delete()

        # repopulate
        populate_rule_components()
        
        # make sure it's gone
        self.assertEqual(LeftSide.objects.filter(display_name="have a new test tagset tag that").count(), 0)

class TestQuerySetGeneration(TestCase, RuleTestAbstractions, QiUnitTestMixin, DestructiveDatabaseTestCase):
    fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        populate_rule_components()

    def _generate_people(self, number=5):
        people = []
        for i in range(0,number):
            people.append(Factory.person().pk)
        people = Person.objects.filter(pk__in=people)
        return people
    
    def _generate_people_with_volunteer_history(self, number=5):
        ppl = self._generate_people(number=number)
        for p in ppl:
            Factory.volunteer_history(p)
        return ppl

    def test_create_new_group_rule_for_general_tag_contains(self, right_hand_term="test", operator_name="contains"):
        # create a new group rule
        group = Factory.group()
        left_side = LeftSide.objects.get(display_name="have a General tag that")
        icontains = Operator.objects.get(display_name=operator_name)
        rst = self._text_right_side_types[0]
        rsv = RightSideValue.objects.create(right_side_type=rst, value=right_hand_term)
        group_rule = GroupRule.objects.create(group=group, left_side=left_side, operator=icontains, right_side_value=rsv)
        new_group_rule = GroupRule.objects.get(pk=group_rule.pk)

        # assert the correct models exist
        self.assertEqual(new_group_rule.group, group)
        self.assertEqual(new_group_rule.left_side, left_side)
        self.assertEqual(new_group_rule.operator, icontains)
        self.assertEqual(new_group_rule.right_side_value, rsv)
        self.assertEqual(new_group_rule.group, group)

        return new_group_rule


    def test_create_new_group_rule_for_custom_tag_is_exactly(self, right_hand_term="test", operator_name="is exactly"):
        # create a new group 
        group = Factory.group()
        
        # make the custom tag
        TagSet.objects.get_or_create(name="new test tagset")
        populate_rule_components()
        # create a new group rule
        left_side = LeftSide.objects.get(display_name="have a new test tagset tag that")
        icontains = Operator.objects.get(display_name=operator_name)
        rst = self._text_right_side_types[0]
        rsv = RightSideValue.objects.create(right_side_type=rst, value=right_hand_term)
        group_rule = GroupRule.objects.create(group=group, left_side=left_side, operator=icontains, right_side_value=rsv)
        new_group_rule = GroupRule.objects.get(pk=group_rule.pk)

        # assert the correct models exist
        self.assertEqual(new_group_rule.group, group)
        self.assertEqual(new_group_rule.left_side, left_side)
        self.assertEqual(new_group_rule.operator, icontains)
        self.assertEqual(new_group_rule.right_side_value, rsv)
        self.assertEqual(new_group_rule.group, group)

        return new_group_rule

    def test_create_new_group_rule_for_last_volunteer_shift_is_on(self, right_hand_term="3/24/2010", operator_name="is on"):
        # create a new group 
        group = Factory.group()
        
        # create a new group rule
        left_side = LeftSide.objects.get(display_name="last volunteer shift")
        op = Operator.objects.get(display_name=operator_name)
        rst = self._date_right_side_types[0]
        rsv = RightSideValue.objects.create(right_side_type=rst, value=right_hand_term)
        group_rule = GroupRule.objects.create(group=group, left_side=left_side, operator=op, right_side_value=rsv)
        new_group_rule = GroupRule.objects.get(pk=group_rule.pk)

        # assert the correct models exist
        self.assertEqual(new_group_rule.group, group)
        self.assertEqual(new_group_rule.left_side, left_side)
        self.assertEqual(new_group_rule.operator, op)
        self.assertEqual(new_group_rule.right_side_value, rsv)
        self.assertEqual(new_group_rule.group, group)

        return new_group_rule


    def test_create_new_group_rule_for_last_donation_is_after(self, right_hand_term="2/12/2009", operator_name="is after"):
       # create a new group 
        group = Factory.group()
        
        # create a new group rule
        left_side = LeftSide.objects.get(display_name="last donation")
        op = Operator.objects.get(display_name=operator_name)
        rst = self._date_right_side_types[0]
        rsv = RightSideValue.objects.create(right_side_type=rst, value=right_hand_term)
        group_rule = GroupRule.objects.create(group=group, left_side=left_side, operator=op, right_side_value=rsv)
        new_group_rule = GroupRule.objects.get(pk=group_rule.pk)

        # assert the correct models exist
        self.assertEqual(new_group_rule.group, group)
        self.assertEqual(new_group_rule.left_side, left_side)
        self.assertEqual(new_group_rule.operator, op)
        self.assertEqual(new_group_rule.right_side_value, rsv)
        self.assertEqual(new_group_rule.group, group)

        return new_group_rule


    def test_create_new_group_rule_for_volunteer_status_is_active(self, right_hand_term="active", operator_name="is"):
        # create a new group 
        group = Factory.group()
        
        # create a new group rule
        left_side = LeftSide.objects.get(display_name="volunteer status")
        icontains = Operator.objects.get(display_name=operator_name)
        rst = self._choices_right_side_types[0]
        rsv = RightSideValue.objects.create(right_side_type=rst, value=right_hand_term)
        group_rule = GroupRule.objects.create(group=group, left_side=left_side, operator=icontains, right_side_value=rsv)
        new_group_rule = GroupRule.objects.get(pk=group_rule.pk)

        # assert the correct models exist
        self.assertEqual(new_group_rule.group, group)
        self.assertEqual(new_group_rule.left_side, left_side)
        self.assertEqual(new_group_rule.operator, icontains)
        self.assertEqual(new_group_rule.right_side_value, rsv)
        self.assertEqual(new_group_rule.group, group)

        return new_group_rule


    # def test_create_new_group_rule_for_volunteer_status_is_inactive(self):
    #     # create a new group rule
    #     # assert the correct models exist
    #     assert True == "Test written"
        


    def test_queryset_for_new_group_rule_for_general_tag_contains(self):
        # create a new group rule (and TagSet)
        group_rule = self.test_create_new_group_rule_for_general_tag_contains()

        # hand-create a few people, some of whom match, and others who don't
        ppl = self._generate_people(number=6)

        TagSet.create_tag_for_person(person=ppl[0], tagset_name="General", tag="really cool test tag")
        TagSet.create_tag_for_person(person=ppl[2], tagset_name="General", tag="really cool test tag")
        TagSet.create_tag_for_person(person=ppl[4], tagset_name="General", tag="another tag")
        TagSet.create_tag_for_person(person=ppl[5], tagset_name="Donor", tag="really cool test tag")

        # assert the queryset string is right
        self.assertEqual(group_rule.queryset_filter_string, "filter(tagsetmembership__in=TagSetMembership.objects.filter(tagset__name='General',taggedtagsetmembership__tag__name__icontains='test'))")

        # get the queryset, make sure it matches a hand-created one.
        qs = group_rule.queryset
    
        hand_qs = Person.objects.filter(Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) )
        self.assertEqualQuerySets(qs,hand_qs)

        # try for the other tag group
        group_rule2 = self.test_create_new_group_rule_for_general_tag_contains(right_hand_term="another")
        hand_qs2 = Person.objects.filter(Q(pk=ppl[4].pk) )
        self.assertEqualQuerySets(group_rule2.queryset,hand_qs2)


    def test_queryset_for_new_group_rule_for_custom_tag_is_exactly(self):
        # hand-create a few people, some of whom match, and others who don't
        ppl = self._generate_people(number=5)

        TagSet.create_tag_for_person(person=ppl[0], tagset_name="new test tagset", tag="really cool test tag")
        TagSet.create_tag_for_person(person=ppl[2], tagset_name="new test tagset", tag="really cool test tag")
        TagSet.create_tag_for_person(person=ppl[4], tagset_name="new test tagset", tag="another tag")

        # create a new group rule
        group_rule = self.test_create_new_group_rule_for_custom_tag_is_exactly()

        # assert the queryset string is right
        self.assertEqual(group_rule.queryset_filter_string, "filter(tagsetmembership__in=TagSetMembership.objects.filter(tagset__name='new test tagset',taggedtagsetmembership__tag__name__iexact='test'))")

        # get the queryset, make sure it matches a hand-created one.
        qs = group_rule.queryset
    
        self.assertEqualQuerySets(qs,Person.objects.none())

        # check the contains group
        opposite_group_rule = self.test_create_new_group_rule_for_custom_tag_is_exactly(right_hand_term="test", operator_name="contains")
        opposite_hand_qs = Person.objects.filter(Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) )
        self.assertEqualQuerySets(opposite_group_rule.queryset,opposite_hand_qs)

        # try for the other tag group
        group_rule2 = self.test_create_new_group_rule_for_custom_tag_is_exactly(right_hand_term="another tag")
        hand_qs2 = Person.objects.filter(Q(pk=ppl[4].pk))
        self.assertEqualQuerySets(group_rule2.queryset,hand_qs2)

    
    def test_queryset_for_new_group_rule_for_last_volunteer_shift_is_on(self):
        # create a new group rule (and TagSet)
        group_rule = self.test_create_new_group_rule_for_last_volunteer_shift_is_on()

        # hand-create a few people, some of whom match, and others who don't
        ppl = self._generate_people()
        target_date = datetime.date(month=3,day=24,year=2010)
        Factory.completed_volunteer_shift(ppl[2], date=target_date)
        Factory.completed_volunteer_shift(ppl[4], date=target_date)

        # assert the queryset string is right
        self.assertEqual(group_rule.queryset_filter_string, "filter(volunteer__completedshift__date=datetime.date(month=3,day=24,year=2010))")

        # get the queryset, make sure it matches a hand-created one.
        qs = group_rule.queryset
    
        hand_qs = Person.objects.filter(Q(pk=ppl[2].pk) | Q(pk=ppl[4].pk) )
        self.assertEqualQuerySets(qs,hand_qs)


    def test_queryset_for_new_group_rule_for_last_donation_is_after(self):
        # create a new group rule
        group_rule = self.test_create_new_group_rule_for_last_donation_is_after()

        # hand-create a few people, some of whom match, and others who don't
        ppl = self._generate_people()
        target_date = datetime.date(month=2,day=12,year=2009)
        Factory.donation(ppl[1], date=target_date+datetime.timedelta(days=10))
        Factory.donation(ppl[2], date=target_date)
        Factory.donation(ppl[4], date=target_date-datetime.timedelta(days=59))

        self.assertEqual(group_rule.queryset_filter_string, "filter(donor__donation__date__gt=datetime.date(month=2,day=12,year=2009))")

        # get the queryset, make sure it matches a hand-created one.
        qs = group_rule.queryset
    
        hand_qs = Person.objects.filter(Q(pk=ppl[1].pk))
        self.assertEqualQuerySets(qs,hand_qs)

        # check the opposite
        opposite_group_rule = self.test_create_new_group_rule_for_last_donation_is_after(operator_name="is before")
        oppostite_hand_qs = Person.objects.filter(Q(pk=ppl[4].pk))
        self.assertEqualQuerySets(opposite_group_rule.queryset,oppostite_hand_qs)



    def test_queryset_for_new_group_rule_for_volunteer_status_is_active(self):
        from volunteers.models import VOLUNTEER_STATII
        # hand-create a few people, some of whom match, and others who don't
        ppl = self._generate_people()
        v = ppl[1].volunteer
        v.status = VOLUNTEER_STATII[1][0]
        v.save()
        v = ppl[3].volunteer
        v.status = VOLUNTEER_STATII[2][0]
        v.save()

        # create a new group rule
        group_rule = self.test_create_new_group_rule_for_volunteer_status_is_active()

        self.assertEqual(group_rule.queryset_filter_string, "filter(volunteer__status='active')")

        # get the queryset, make sure it matches a hand-created one.
        qs = group_rule.queryset
        hand_qs = Person.objects.filter(Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) | Q(pk=ppl[4].pk))

        self.assertEqualQuerySets(qs,hand_qs)

        # check the opposite
        opposite_group_rule = self.test_create_new_group_rule_for_volunteer_status_is_active(operator_name="is not")
        oppostite_hand_qs = Person.objects.filter(Q(pk=ppl[1].pk) | Q(pk=ppl[3].pk))
        self.assertEqualQuerySets(opposite_group_rule.queryset,oppostite_hand_qs)



    # def test_queryset_for_new_group_rule_for_volunteer_status_is_inactive(self):
    #     # hand-create a few people, some of whom match, and others who don't. Include temporarily inactive
    #     # create a new group rule
    #     self.test_create_new_group_rule_for_volunteer_status_is_inactive()
    #     # assert the queryset string is right
    #     # get the queryset, make sure it matches a hand-created one.


    # def test_queryset_total_volunteer_hours_in_the_last_12_months(self):
    #     # hand-create a few people, some of whom match, and others who don't. Include temporarily inactive
    #     # create a new group rule
    #     self.test_create_new_group_rule_for_volunteer_status_is_inactive()
    #     # assert the queryset string is right
    #     # get the queryset, make sure it matches a hand-created one.

    # def test_queryset_total_donations_in_the_last_12_months(self):
    #     # hand-create a few people, some of whom match, and others who don't. Include temporarily inactive
    #     # create a new group rule
    #     self.test_create_new_group_rule_for_volunteer_status_is_inactive()
    #     # assert the queryset string is right
    #     # get the queryset, make sure it matches a hand-created one.

    def test_invalid_rule_missing_left_side(self):
        assert True == "test written"

    def test_invalid_rule_missing_operator_side(self):
        assert True == "test written"
        
    def test_invalid_rule_missing_right_side(self):
        assert True == "test written"