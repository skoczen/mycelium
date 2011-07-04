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
