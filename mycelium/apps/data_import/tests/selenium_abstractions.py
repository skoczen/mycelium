# encoding: utf-8
import time
from test_factory import Factory
from django.conf import settings
import os
from accounts.tests.selenium_abstractions import _sitespaced_url
from spreadsheets.spreadsheet import EXCEL_TYPE, CSV_TYPE
from spreadsheets.spreadsheet import SpreadsheetAbstraction
from data_import.tests.abstractions import TEST_SPREADSHEET_PATH
from people.models import Person

class DataImportTestAbstractions(object):

    def get_to_import_list(self):
        sel = self.selenium
        self.open("/")
        sel.wait_for_page_to_load(30000)
        sel.click("css=.admin_btn")
        sel.wait_for_page_to_load(30000)
        sel.click("css=.data_import_btn")
        sel.wait_for_page_to_load(30000)
        assert sel.is_text_present("Data Import History")

    def get_to_start_import_page(self):
        self.get_to_import_list()
        sel = self.selenium
        sel.click("css=.start_import_btn")
        sel.wait_for_page_to_load(30000)
        assert sel.is_text_present("Start Data Import")

    def set_upload_file(self, filename):
        sel = self.selenium
        sel.attach_file("css=.qq-uploader input[name=file]", "http://127.0.0.1:8199/%s" % (filename, ))

    def create_and_save_200_person_spreadsheet(self, fields=["first_name","last_name","email","phone_number"], spreadsheet_filename=None):
        if not spreadsheet_filename:
            spreadsheet_filename = "test.xls"
        
        full_filename = os.path.join(settings.PROJECT_ROOT, TEST_SPREADSHEET_PATH, spreadsheet_filename)
        
        

        if not os.path.exists(full_filename):
            Person.objects_by_account(self.account).all().delete()
            [Factory.person(self.account) for f in range(0,200)]
            fh = open(full_filename, 'w')
            q = Person.objects_by_account(self.account).all()

            SpreadsheetAbstraction.create_spreadsheet(q, fields, EXCEL_TYPE, file_handler=fh)
            fh.flush()
            fh.close()
        
        Person.objects_by_account(self.account).all().delete()

        return spreadsheet_filename
