import time
from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase
from groups.models import Group
from people.models import Person, Organization, Employee
from donors.models import Donor, Donation
from accounts.models import Account
from volunteers.models import Volunteer, CompletedShift
from generic_tags.models import TagSet, Tag
from django.core import mail

class Dummy(object):
    pass

class TestAccountFactory(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase):
    # fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        pass

    
    def test_challenge_has_imported_contacts(self):
        assert True == "Test written"
        
    def test_challenge_has_set_up_tags(self):
        assert True == "Test written"
        
    def test_challenge_has_added_board(self):
        assert True == "Test written"
        
    def test_challenge_has_created_other_accounts(self):
        assert True == "Test written"
        
    def test_challenge_has_downloaded_spreadsheet(self):
        assert True == "Test written"
        
    def test_challenge_submitted_support(self):
        assert True == "Test written"
        
    def test_has_completed_all_challenges(self):
        assert True == "Test written"
        
    def test_has_completed_any_challenges(self):
        assert True == "Test written"
        
