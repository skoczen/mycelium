import time
import datetime
from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase
from groups.models import Group
from people.models import Person
from organizations.models import Organization, Employee
from donors.models import Donor, Donation
from accounts.models import Account, UserAccount, AccessLevel
from volunteers.models import Volunteer, CompletedShift
from generic_tags.models import TagSet, Tag
from django.core import mail
from django.test.client import Client
from accounts import CANCELLED_SUBSCRIPTION_STATII

class Dummy(object):
    pass

class TestFlightControl(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase):
    # fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        pass

    # def test_factory_account_can_be_run_multiple_times(self):
    #     for i in range(0,Factory.rand_int(2,6)):
    #         Factory.create_demo_site("test%s" % i, quick=True)

    #     assert True == True # Finished successfully.        
