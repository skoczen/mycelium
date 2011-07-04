from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase
from people.models import Person
from volunteers import VOLUNTEER_STATII
import datetime
from groups.tests import GroupTestAbstractions
from rules.tests import RuleTestAbstractions
from accounts.tests.selenium_abstractions import AccountTestAbstractions

class Dummy(object):
    pass

class TestBirthdays(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase, AccountTestAbstractions):
    # fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        self.account = self.create_demo_site("test",mostly_empty=True)
        self.request = Dummy()
        self.request.account = self.account

    def tearDown(self):
        self.account.delete()

    def test_age_and_next_age(self):
        today = datetime.date.today()
        today_20_years_ago = datetime.date(year=today.year-20, day=today.day, month=today.month)

        yesterday_20_years_ago = today_20_years_ago - datetime.timedelta(days=1)
        tomorrow_20_years_ago = today_20_years_ago + datetime.timedelta(days=1)

        p1 = Factory.person(account=self.account, birthday=yesterday_20_years_ago)
        p2 = Factory.person(account=self.account, birthday=today_20_years_ago)
        p3 = Factory.person(account=self.account, birthday=tomorrow_20_years_ago)
        p4 = Factory.person(account=self.account)
        p4.birth_year = None
        p4.birth_day = 4
        p4.birth_month = 9
        p4.save()

        self.assertEqual(p1.age, 20)
        self.assertEqual(p2.age, 20)
        self.assertEqual(p3.age, 19)
        self.assertEqual(p4.age, None)
        self.assertEqual(p1.next_or_todays_birthday_age, 21)
        self.assertEqual(p2.next_or_todays_birthday_age, 20)
        self.assertEqual(p3.next_or_todays_birthday_age, 20)
        self.assertEqual(p4.next_or_todays_birthday_age, None)