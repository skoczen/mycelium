import time
import datetime
from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase
from groups.models import Group
from data_import.models import DataImport, Spreadsheet, ImportSpreadsheet
class Dummy(object):
    pass

class TestDataImport(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase):
    # fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        self.a1 = Factory.create_demo_site("test1", quick=True, mostly_empty=True)

    # def test_challenge_has_imported_contacts(self):
    #     self.a1.check_challenge_progress()
    #     assert self.a1.challenge_has_imported_contacts == True
        
