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

    def choose_person_as_import_type(self):
        sel = self.selenium
        assert not sel.is_element_present("css=.qq-upload-button")
        sel.click("css=.import_type_people input")
        sel.wait_for_element_present("css=.qq-upload-button")
    
    def start_person_spreadsheet_upload(self):
        sel = self.selenium
        filename = self.create_and_save_200_person_spreadsheet()
        self.choose_person_as_import_type()
        self.set_upload_file(filename)
        sel.wait_for_element_present("css=.qq-upload-success")
        sel.select("css=.import_fields_confirmation th.col_0 select", "First Name")
        sel.select("css=.import_fields_confirmation th.col_1 select", "Last Name")
        sel.select("css=.import_fields_confirmation th.col_2 select", "Phone")
        sel.select("css=.import_fields_confirmation th.col_3 select", "Email")
        time.sleep(0.2)
        sel.click("css=.submit_and_start_import_btn")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Right now")

    def upload_person_spreadsheet_successfully(self):
        sel = self.selenium
        self.start_person_spreadsheet_upload()

        start_time = time.time()
        success = False
        while time.time() - start_time < 120  and not success:
            if sel.is_text_present("View Results"):
                success = True
            else:
                time.sleep(10)
        
        assert success == True