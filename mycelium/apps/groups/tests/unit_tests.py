from test_factory import Factory
from nose.tools import istest
from rules.models import LeftSide, Operator, RightSideType, RightSideValue, Rule
from rules.tasks import populate_rule_components
from groups.models import GroupRule
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase
from people.models import Person, NO_NAME_STRING

class GroupTestAbstractions(object):
    pass

class TestQuerySetGeneration(TestCase, GroupTestAbstractions, QiUnitTestMixin, DestructiveDatabaseTestCase):
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

    def test_full_name(self):
        # create a new group rule
        group = Factory.group()
        self.assertEqual(group.name, group.full_name)
        
        group.name = None
        group.save()
        
        self.assertEqual(NO_NAME_STRING, group.full_name)

    def test_searchable_name(self):
        # create a new group rule
        group = Factory.group()
        self.assertEqual(group.name, group.searchable_name)

        group.name = None
        group.save()
        
        self.assertEqual("", group.searchable_name)

    def test_members(self):
        # create a new group rule
        group = Factory.group()


    def test_active_volunteers_with_shift_in_last_6_months(self):
        # create the people
        # check the qs active volunteer rule added

        # check the qs after last_shift added
        pass

    def test_any_tag_test_donor_tag_major(self):
        # create the people
        # check the qs test tag rule added

        # check the qs after both rules added
        pass

    def test_custom_tag_and_last_donation_one_month_ago(self):
        # create the people
        # check the qs active volunteer rule added

        # check the qs after last_shift added
        pass
