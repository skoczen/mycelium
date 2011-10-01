from test_factory import Factory
from rules.models import LeftSide, Operator
from rules.tasks import populate_rule_components_for_an_account
from groups.models import GroupRule, NO_NAME_STRING_GROUP
from djangosanetesting.cases import DestructiveDatabaseTestCase
from functional_tests.selenium_test_case import DjangoFunctionalUnitTestMixin
from django.db.models import Q
from django.test import TestCase
from people.models import Person
from volunteers import VOLUNTEER_STATII
import datetime
from groups.tests import GroupTestAbstractions
from rules.tests import RuleTestAbstractions
from accounts.tests.selenium_abstractions import AccountTestAbstractions

class Dummy(object):
    pass

class TestQuerySetGeneration(TestCase, GroupTestAbstractions, DjangoFunctionalUnitTestMixin, DestructiveDatabaseTestCase, RuleTestAbstractions, AccountTestAbstractions):
    # fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        self.account = self.create_demo_site("test",mostly_empty=True)
        self.request = Dummy()
        self.request.account = self.account
        populate_rule_components_for_an_account(self.account)

    def tearDown(self):
        self.account.delete()

    def _generate_people(self, number=5):
        people = []
        for i in range(0,number):
            p = Factory.person(self.account)
            v = p.volunteer
            v.status = VOLUNTEER_STATII[1][0]
            v.save()
            people.append(p.pk)
        people = Person.objects_by_account(self.account).filter(pk__in=people)
        return people
    
    def _generate_people_with_volunteer_history(self, number=5):
        ppl = self._generate_people(number=number)
        for p in ppl:
            Factory.volunteer_history(p)
        return ppl

    def test_full_name(self):
        # create a new group rule
        group = Factory.group(self.account,)
        self.assertEqual(group.name, group.full_name)
        
        group.name = None
        group.save()
        
        self.assertEqual(NO_NAME_STRING_GROUP, group.full_name)

    def test_searchable_name(self):
        # create a new group rule
        group = Factory.group(self.account,)
        self.assertEqual(group.name, group.searchable_name)

        group.name = None
        group.save()
        
        self.assertEqual("", group.searchable_name)

    def test_members(self):
        # create a new group
        group = Factory.group(self.account,)
        self._generate_people()
        all_ppl_qs = Person.objects_by_account(self.account).none()

        self.assertEqualQuerySets(group.members, all_ppl_qs)




    def test_active_volunteers_and_with_shift_after_date(self):
        # create the people
        group = Factory.group(self.account)
        ppl = self._generate_people()
        v = ppl[1].volunteer
        v.status = VOLUNTEER_STATII[2][0]  #inactive
        v.save()
        v = ppl[3].volunteer
        v.status = VOLUNTEER_STATII[3][0]  #temporarily inactive
        target_date = datetime.date(month=3,day=24,year=2010)
        Factory.completed_volunteer_shift(ppl[2], date=target_date)
        v.save()        
        
        # things got properly cleaned up
        self.assertEqual( Person.objects_by_account(self.account).count(), 5)
        self.assertEqual( Person.raw_objects.count() , 5)

        all_ppl_qs = Person.objects_by_account(self.account).none()
        active_volunteer_qs = Person.objects_by_account(self.account).filter(Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) | Q(pk=ppl[4].pk))
        active_volunteer_with_shift = Person.objects_by_account(self.account).filter( Q(pk=ppl[2].pk) )

        self.assertEqualQuerySets(group.members, all_ppl_qs)

        # check the qs active volunteer rule added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="volunteer status")
        icontains = Operator.objects_by_account(self.account).get(display_name="is")
        rst = self._choices_right_side_types[0]
        rsv ="active"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)

        self.assertEqualQuerySets(group.members, active_volunteer_qs)

        # check the qs after last_shift added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="last volunteer shift")
        icontains = Operator.objects_by_account(self.account).get(display_name="is after")
        rst = self._date_right_side_types[0]
        rsv ="1/15/2010"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)


        self.assertEqualQuerySets(group.members, active_volunteer_with_shift)

    def test_any_tag_test_and_donor_tag_major(self):
        # create the people
        group = Factory.group(self.account,)
        ppl = self._generate_people()
        self.create_tag_for_person(person=ppl[0], tagset_name="new test tagset", tag="really cool test tag")
        self.create_tag_for_person(person=ppl[2], tagset_name="new test tagset", tag="really cool test tag")
        self.create_tag_for_person(person=ppl[4], tagset_name="new test tagset", tag="another tag")
        self.create_tag_for_person(person=ppl[2], tagset_name="Donor", tag="major")
        self.create_tag_for_person(person=ppl[3], tagset_name="Donor", tag="major")
        

        all_ppl_qs = Person.objects_by_account(self.account).none()
        test_tag_qs = Person.objects_by_account(self.account).filter(Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) )
        test_and_donor_tag_qs = Person.objects_by_account(self.account).filter( Q(pk=ppl[2].pk) )
        #test_donor_qs = Person.objects_by_account(self.account).filter( Q(pk=ppl[2].pk) | Q(pk=ppl[3].pk))

        self.assertEqualQuerySets(group.members, all_ppl_qs)

        # check the qs active volunteer rule added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="have any tag that")
        icontains = Operator.objects_by_account(self.account).get(display_name="contains")
        rst = self._text_right_side_types[0]
        rsv ="test"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)

        self.assertEqualQuerySets(group.members, test_tag_qs)

        # check the qs after last_shift added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="have a Donor tag that")
        icontains = Operator.objects_by_account(self.account).get(display_name="is exactly")
        rst = self._text_right_side_types[0]
        rsv ="major"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)

        # self.assertEqualQuerySets(group.members, test_donor_qs)

        self.assertEqualQuerySets(group.members, test_and_donor_tag_qs)

    def test_custom_tag_and_last_donation_one_month_ago(self):
        # create the people
        group = Factory.group(self.account,)
        ppl = self._generate_people()
        self.create_tag_for_person(person=ppl[0], tagset_name="new test tagset", tag="really cool test tag")
        self.create_tag_for_person(person=ppl[2], tagset_name="new test tagset", tag="really cool test tag")
        self.create_tag_for_person(person=ppl[4], tagset_name="new test tagset", tag="another tag")
        target_date = datetime.date(month=3,day=24,year=2010)
        Factory.donation(ppl[0], date=target_date-datetime.timedelta(days=600))
        Factory.donation(ppl[1], date=target_date-datetime.timedelta(days=600))
        Factory.donation(ppl[2], date=target_date)
        Factory.donation(ppl[3], date=target_date-datetime.timedelta(days=7))
        

        all_ppl_qs = Person.objects_by_account(self.account).none()
        test_tag_qs = Person.objects_by_account(self.account).filter(Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) )
        test_and_donation_tag_qs = Person.objects_by_account(self.account).filter( Q(pk=ppl[2].pk) )

        self.assertEqualQuerySets(group.members, all_ppl_qs)

        # check the qs active volunteer rule added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="have a new test tagset tag that")
        icontains = Operator.objects_by_account(self.account).get(display_name="contains")
        rst = self._text_right_side_types[0]
        rsv ="test"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)

        self.assertEqualQuerySets(group.members, test_tag_qs)

        # check the qs after last_shift added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="last donation")
        icontains = Operator.objects_by_account(self.account).get(display_name="is after")
        rst = self._date_right_side_types[0]
        rsv ="02/05/2010"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)


        self.assertEqualQuerySets(group.members, test_and_donation_tag_qs)


    def test_active_volunteers_or_with_shift_after_date(self):
        # create the people
        group = Factory.group(self.account,rules_boolean=False)
        ppl = self._generate_people()
        v = ppl[1].volunteer
        v.status = VOLUNTEER_STATII[2][0]  #inactive
        v.save()
        v = ppl[3].volunteer
        v.status = VOLUNTEER_STATII[3][0]  #temporarily inactive
        target_date = datetime.date(month=3,day=24,year=2010)
        v.save()        
        Factory.completed_volunteer_shift(ppl[2], date=target_date)
        Factory.completed_volunteer_shift(ppl[3], date=target_date)

        all_ppl_qs = Person.objects_by_account(self.account).none()
        active_volunteer_qs = Person.objects_by_account(self.account).filter(Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) | Q(pk=ppl[4].pk))
        active_volunteer_with_shift = Person.objects_by_account(self.account).filter( Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) | Q(pk=ppl[4].pk) | Q(pk=ppl[3].pk) )

        self.assertEqualQuerySets(group.members, all_ppl_qs)

        # check the qs active volunteer rule added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="volunteer status")
        icontains = Operator.objects_by_account(self.account).get(display_name="is")
        rst = self._choices_right_side_types[0]
        rsv ="active"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)

        self.assertEqualQuerySets(group.members, active_volunteer_qs)

        # check the qs after last_shift added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="last volunteer shift")
        icontains = Operator.objects_by_account(self.account).get(display_name="is after")
        rst = self._date_right_side_types[0]
        rsv ="1/15/2010"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)


        self.assertEqualQuerySets(group.members, active_volunteer_with_shift)

    def test_any_tag_test_or_donor_tag_major(self):
        # create the people
        group = Factory.group(self.account,rules_boolean=False)
        ppl = self._generate_people()
        self.create_tag_for_person(person=ppl[0], tagset_name="new test tagset", tag="really cool test tag")
        self.create_tag_for_person(person=ppl[2], tagset_name="new test tagset", tag="really cool test tag")
        self.create_tag_for_person(person=ppl[4], tagset_name="new test tagset", tag="another tag")
        self.create_tag_for_person(person=ppl[2], tagset_name="Donor", tag="major")
        self.create_tag_for_person(person=ppl[3], tagset_name="Donor", tag="major")
        

        all_ppl_qs = Person.objects_by_account(self.account).none()
        test_tag_qs = Person.objects_by_account(self.account).filter(Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) )
        test_and_donor_tag_qs = Person.objects_by_account(self.account).filter( Q(pk=ppl[2].pk) | Q(pk=ppl[0].pk) | Q(pk=ppl[3].pk)  )

        self.assertEqualQuerySets(group.members, all_ppl_qs)

        # check the qs active volunteer rule added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="have any tag that")
        icontains = Operator.objects_by_account(self.account).get(display_name="contains")
        rst = self._text_right_side_types[0]
        rsv ="test"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)

        self.assertEqualQuerySets(group.members, test_tag_qs)

        # check the qs after last_shift added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="have a Donor tag that")
        icontains = Operator.objects_by_account(self.account).get(display_name="is exactly")
        rst = self._text_right_side_types[0]
        rsv ="major"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)


        self.assertEqualQuerySets(group.members, test_and_donor_tag_qs)

    def test_custom_tag_or_last_donation_one_month_ago(self):
        # create the people
        group = Factory.group(self.account,rules_boolean=False)
        ppl = self._generate_people()
        self.create_tag_for_person(person=ppl[0], tagset_name="new test tagset", tag="really cool test tag")
        self.create_tag_for_person(person=ppl[2], tagset_name="new test tagset", tag="really cool test tag")
        self.create_tag_for_person(person=ppl[4], tagset_name="new test tagset", tag="another tag")
        
        target_date = datetime.date(month=3,day=24,year=2010)
        Factory.donation(ppl[0], date=target_date-datetime.timedelta(days=600))
        Factory.donation(ppl[1], date=target_date-datetime.timedelta(days=600))
        Factory.donation(ppl[2], date=target_date)
        Factory.donation(ppl[3], date=target_date-datetime.timedelta(days=7))
        

        all_ppl_qs = Person.objects_by_account(self.account).none()
        test_tag_qs = Person.objects_by_account(self.account).filter(Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) )
        test_and_donation_tag_qs = Person.objects_by_account(self.account).filter( Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) | Q(pk=ppl[3].pk) )


        self.assertEqualQuerySets(group.members, all_ppl_qs)

        # check the qs active volunteer rule added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="have a new test tagset tag that")
        icontains = Operator.objects_by_account(self.account).get(display_name="contains")
        rst = self._text_right_side_types[0]
        rsv ="test"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)

        self.assertEqualQuerySets(group.members, test_tag_qs)

        # check the qs after last_shift added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="last donation")
        icontains = Operator.objects_by_account(self.account).get(display_name="is after")
        rst = self._date_right_side_types[0]
        rsv ="02/05/2010"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)

        # test_donation_qs = Person.objects_by_account(self.account).filter( Q(pk=ppl[2].pk) | Q(pk=ppl[3].pk) )
        # self.assertEqualQuerySets(group.members, test_donation_qs)

        self.assertEqualQuerySets(group.members, test_and_donation_tag_qs)

    def test_custom_tag_or_last_donation_one_month_ago_with_an_invalid_rules(self):
        # create the people
        group = Factory.group(self.account,rules_boolean=False)
        ppl = self._generate_people()
        self.create_tag_for_person(person=ppl[0], tagset_name="new test tagset", tag="really cool test tag")
        self.create_tag_for_person(person=ppl[2], tagset_name="new test tagset", tag="really cool test tag")
        self.create_tag_for_person(person=ppl[4], tagset_name="new test tagset", tag="another tag")
        target_date = datetime.date(month=3,day=24,year=2010)
        Factory.donation(ppl[0], date=target_date-datetime.timedelta(days=600))
        Factory.donation(ppl[1], date=target_date-datetime.timedelta(days=600))
        Factory.donation(ppl[2], date=target_date)
        Factory.donation(ppl[3], date=target_date-datetime.timedelta(days=7))
        

        all_ppl_qs = Person.objects_by_account(self.account).none()
        test_tag_qs = Person.objects_by_account(self.account).filter(Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) )
        test_and_donation_tag_qs = Person.objects_by_account(self.account).filter( Q(pk=ppl[0].pk) | Q(pk=ppl[2].pk) | Q(pk=ppl[3].pk) )

        self.assertEqualQuerySets(group.members, all_ppl_qs)

        # check the qs active volunteer rule added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="have a new test tagset tag that")
        icontains = Operator.objects_by_account(self.account).get(display_name="contains")
        rst = self._text_right_side_types[0]
        rsv ="test"
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)

        self.assertEqualQuerySets(group.members, test_tag_qs)

        # check the qs after last_shift added
        left_side = LeftSide.objects_by_account(self.account).get(display_name="last donation")
        icontains = Operator.objects_by_account(self.account).get(display_name="is after")
        rst = self._date_right_side_types[0]
        rsv ="02/05/2010"
        GroupRule.objects_by_account(self.account).create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)


        self.assertEqualQuerySets(group.members, test_and_donation_tag_qs)


        # add a rule missing a right side value
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=None)
        self.assertEqualQuerySets(group.members, test_and_donation_tag_qs)

        # add a rule missing an operator
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=None, right_side_value=rsv, right_side_type=rst)
        self.assertEqualQuerySets(group.members, test_and_donation_tag_qs)

        # add a rule missing a left side
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=None, operator=icontains, right_side_value=rsv, right_side_type=rst)
        self.assertEqualQuerySets(group.members, test_and_donation_tag_qs)

        # add a rule missing everything
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=None, operator=None, right_side_value=None)
        self.assertEqualQuerySets(group.members, test_and_donation_tag_qs)

    def test_has_a_valid_rule_function(self):
        group = Factory.group(self.account,rules_boolean=False)
        left_side = LeftSide.objects_by_account(self.account).get(display_name="last donation")
        icontains = Operator.objects_by_account(self.account).get(display_name="is after")
        rst = self._date_right_side_types[0]
        rsv = "02/05/2010"

        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=None)
        self.assertEqual(group.has_a_valid_rule, False)

        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=None, right_side_type=rst)
        self.assertEqual(group.has_a_valid_rule, False)

        # add a rule missing an operator
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=None, right_side_value=rsv, right_side_type=rst)
        self.assertEqual(group.has_a_valid_rule, False)

        # add a rule missing a left side
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=None, operator=icontains, right_side_value=rsv, right_side_type=rst)
        self.assertEqual(group.has_a_valid_rule, False)

        # add a rule missing everything
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=None, operator=None, right_side_value=None,  right_side_type=None)
        self.assertEqual(group.has_a_valid_rule, False)

        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)
        self.assertEqual(group.has_a_valid_rule, True)
    
    def test_age_group(self):
        group = Factory.group(self.account,rules_boolean=False)
        left_side = LeftSide.objects_by_account(self.account).get(display_name="age")
        icontains = Operator.objects_by_account(self.account).get(display_name="is less than")
        rst = self._number_right_side_types[0]
        rsv ="50"
        self._generate_people(number=50)
        
        GroupRule.raw_objects.create(account=self.account, group=group, left_side=left_side, operator=icontains, right_side_value=rsv, right_side_type=rst)
        self.assertEqual(group.has_a_valid_rule, True)

        birthday_qs = Person.objects.filter(actual_birthday__gt=datetime.datetime.now()-datetime.timedelta(days=365.25*50))
        self.assertEqualQuerySets(group.members, birthday_qs)



        