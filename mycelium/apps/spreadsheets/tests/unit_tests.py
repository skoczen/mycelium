import time
import datetime
import unittest
import os
from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase
from django.conf import settings
from groups.models import Group
from data_import.models import DataImport
from spreadsheets.spreadsheet import SpreadsheetAbstraction, EXCEL_TYPE, CSV_TYPE
from data_import.tests.abstractions import GenerateSpreadsheetsMixin, TEST_SPREADSHEET_PATH
from people.models import Person


class Dummy(object):
    pass

class TestViews(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase, GenerateSpreadsheetsMixin):

    def setUp(self):
        self.a1 = Factory.create_demo_site("test1", quick=True)

    def test_full_contact_list_spreadsheet(self):
        # starting place
        people_info = [self._person_dict(p) for p in Person.objects_by_account(self.a1)]

        from spreadsheets.views import download
        assert True == "Test finished"