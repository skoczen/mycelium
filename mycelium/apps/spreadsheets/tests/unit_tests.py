import time
import datetime
import unittest
import os
from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from functional_tests.selenium_test_case import DjangoFunctionalUnitTestMixin
from django.test import TestCase
from django.conf import settings
from groups.models import Group
from data_import.models import DataImport
from spreadsheets.spreadsheet import SpreadsheetAbstraction, EXCEL_TYPE, CSV_TYPE
from data_import.tests.abstractions import GenerateSpreadsheetsMixin, TEST_SPREADSHEET_PATH
from django.core.urlresolvers import reverse
from spreadsheets import SPREADSHEET_TEMPLATE_CHOICES

from django.test.client import RequestFactory

from people.models import Person
from donors.models import Donation
from volunteers.models import CompletedShift

class Dummy(object):
    pass

class TestViews(TestCase, DjangoFunctionalUnitTestMixin, DestructiveDatabaseTestCase, GenerateSpreadsheetsMixin):

    def setUp(self):
        self.a1 = Factory.create_demo_site("test1", quick=True)
        self.factory = RequestFactory()
    
    @property
    def _db_identity_set(self):
        s = []
        s.append([self._person_dict(p) for p in Person.objects_by_account(self.a1)])
        s.append([self._donation_dict(d) for d in Donation.objects_by_account(self.a1)])
        s.append([self._shift_dict(c) for c in CompletedShift.objects_by_account(self.a1)])
        return s

    def _test_spreadsheet_download_200s_for_template_type(self, template_type, file_type=None):
        from spreadsheets.views import download
        spreadsheet = Factory.spreadsheet(self.a1, template_type, file_type=file_type)

        request = self.factory.get("%s?type=%s&spreadsheet_id=%s" % (reverse("spreadsheets:download"), spreadsheet.default_filetype, spreadsheet.pk))
        request.account = self.a1

        response = download(request)
        self.assertEqual(response.status_code, 200)

    def test_full_contact_list_spreadsheet_200s(self):
        self._test_spreadsheet_download_200s_for_template_type(SPREADSHEET_TEMPLATE_CHOICES[0][0])

    def test_mailing_list_spreadsheet_200s(self):
        self._test_spreadsheet_download_200s_for_template_type(SPREADSHEET_TEMPLATE_CHOICES[1][0])

    def test_email_list_spreadsheet_200s(self):
        self._test_spreadsheet_download_200s_for_template_type(SPREADSHEET_TEMPLATE_CHOICES[2][0])

    def test_donations_spreadsheet_200s(self):
        self._test_spreadsheet_download_200s_for_template_type(SPREADSHEET_TEMPLATE_CHOICES[3][0])

    def test_donation_summary_spreadsheet_200s(self):
        self._test_spreadsheet_download_200s_for_template_type(SPREADSHEET_TEMPLATE_CHOICES[4][0])

    def test_volunteer_hours_spreadsheet_200s(self):
        self._test_spreadsheet_download_200s_for_template_type(SPREADSHEET_TEMPLATE_CHOICES[5][0])

    def test_volunteer_hour_summary_spreadsheet_200s(self):
        self._test_spreadsheet_download_200s_for_template_type(SPREADSHEET_TEMPLATE_CHOICES[6][0])

    def test_full_contact_list_excel_spreadsheet_with_unicode_200s(self):
        p = Factory.person(account=self.a1)
        p.last_name = u"O\u2019Brien"
        p.save()
        self._test_spreadsheet_download_200s_for_template_type(SPREADSHEET_TEMPLATE_CHOICES[0][0], file_type=EXCEL_TYPE)

    def test_full_contact_list_csv_spreadsheet_with_unicode_200s(self):
        p = Factory.person(account=self.a1)
        p.last_name = u"O\u2019Brien"
        p.save()
        self._test_spreadsheet_download_200s_for_template_type(SPREADSHEET_TEMPLATE_CHOICES[0][0], file_type=CSV_TYPE)
