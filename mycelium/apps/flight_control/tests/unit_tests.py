import time
import datetime
from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from functional_tests.selenium_test_case import DjangoFunctionalUnitTestMixin
from django.test import TestCase
from groups.models import Group
from people.models import Person
from organizations.models import Organization, Employee
from donors.models import Donor, Donation
from accounts.models import Account, UserAccount, AccessLevel
from volunteers.models import Volunteer, CompletedShift
from generic_tags.models import TagSet, Tag, TaggedItem
from spreadsheets.models import Spreadsheet
from conversations.models import Conversation
from django.core import mail
from django.test.client import Client
from accounts import CANCELLED_SUBSCRIPTION_STATII

class Dummy(object):
    pass

class TestFlightControl(TestCase, DjangoFunctionalUnitTestMixin, DestructiveDatabaseTestCase):
    # fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        self.a1 = Factory.create_demo_site("test1", verbose=False, quick=True)
        self.a2 = Factory.create_demo_site("test2", with_demo_flag=False, verbose=False, quick=True)
        
    def test_all_non_demo_accounts_total_volunteer_hours(self):
        total_volunteer_hours = 0
        for c in CompletedShift.objects.filter(account__is_demo=False):
            total_volunteer_hours += c.duration

        self.assertEqual(Account.all_non_demo_accounts_total_volunteer_hours, total_volunteer_hours)

    def test_all_non_demo_accounts_total_donation_amount(self):
        total_donations = 0
        for d in Donation.objects.filter(account__is_demo=False):
            total_donations += d.amount

        self.assertEqual(Account.all_non_demo_accounts_total_donation_amount, total_donations)


    def test_num_non_demo_accounts(self):
        self.assertEqual(Account.num_non_demo_accounts, 1)
        self.a1.delete()
        self.assertEqual(Account.num_non_demo_accounts, 1)
        self.a2.delete()
        self.assertEqual(Account.num_non_demo_accounts, 0)

    def test_num_non_demo_accounts_denominator(self):
        self.assertEqual(Account.num_non_demo_accounts_denominator, 1)
        self.a1.delete()
        self.assertEqual(Account.num_non_demo_accounts_denominator, 1)
        self.a2.delete()
        self.assertEqual(Account.num_non_demo_accounts_denominator, 1)

    def test_all_non_demo_accounts_average_num_users(self):
        self.assertEqual(Account.all_non_demo_accounts_average_num_users, 3)
        self.a1.delete()
        self.a2.delete()
        self.assertEqual(Account.all_non_demo_accounts_average_num_users, 0)
        
    def test_all_non_demo_accounts_average_num_people(self):
        avg = Person.objects.all().filter(account__is_demo=False).count() / Account.num_non_demo_accounts
        self.assertEqual(Account.all_non_demo_accounts_average_num_people, avg)
    
    def test_all_non_demo_accounts_average_num_organizations(self):
        avg = Organization.objects.all().filter(account__is_demo=False).count() / Account.num_non_demo_accounts
        self.assertEqual(Account.all_non_demo_accounts_average_num_organizations, avg)
        
    def test_all_non_demo_accounts_average_donation_amount(self):
        avg = Account.all_non_demo_accounts_total_donation_amount / Account.num_non_demo_accounts
        self.assertEqual(Account.all_non_demo_accounts_average_donation_amount, avg)

    def test_all_non_demo_accounts_average_volunteer_hours(self):
        avg = Account.all_non_demo_accounts_total_volunteer_hours / Account.num_non_demo_accounts
        self.assertEqual(Account.all_non_demo_accounts_average_volunteer_hours_per_account, avg)


    def test_all_non_demo_accounts_num_total_donations(self):
        self.assertEqual(Account.all_non_demo_accounts_num_total_donations, Donation.objects.filter(account__is_demo=False).count())

    def test_all_non_demo_accounts_num_tags(self):
        self.assertEqual(Account.all_non_demo_accounts_num_tags, Tag.objects.filter(account__is_demo=False).count())

    def test_all_non_demo_accounts_num_taggeditems(self):
        self.assertEqual(Account.all_non_demo_accounts_num_tagged_items, TaggedItem.objects.filter(account__is_demo=False).count())

    def test_all_non_demo_accounts_num_groups(self):
        self.assertEqual(Account.all_non_demo_accounts_num_total_groups, Group.objects.filter(account__is_demo=False).count())

    def test_all_non_demo_accounts_num_spreadsheets(self):
        self.assertEqual(Account.all_non_demo_accounts_num_total_spreadsheets, Spreadsheet.objects.filter(account__is_demo=False).count())

    def test_all_non_demo_accounts_num_conversations(self):
        self.assertEqual(Account.all_non_demo_accounts_total_number_of_conversations, Conversation.objects.filter(account__is_demo=False).count())




