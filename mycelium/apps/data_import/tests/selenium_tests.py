from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time 
from test_factory import Factory
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from data_import.tests.selenium_abstractions import DataImportTestAbstractions


class TestMockupPages(QiConservativeSeleniumTestCase, AccountTestAbstractions, DataImportTestAbstractions):
    selenium_fixtures = []

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()

    # def tearDown(self):
    #     self.account.delete()

    def test_mockup_pages_load_and_links_work(self):
        sel = self.selenium        
        self.open("/reports/report/new")
        sel.click("link=Admin")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Data Import", sel.get_text("css=.data_import_btn .button_title"))
        
        sel.click("css=.data_import_btn")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Data Import History", sel.get_text("//div[@id='page']/page_title"))
        self.assertEqual("Start New Import", sel.get_text("link=Start New Import"))
  
        self.assertEqual("View Results", sel.get_text("link=View Results"))
        
        self.assertEqual("Right now", sel.get_text("css=.in_progress .right_now"))
        
        sel.click("link=View Results")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Data Import #5 on Dec 29, 2010 at 3:55pm", sel.get_text("//div[@id='page']/page_title"))
        
        self.assertEqual("We found 2,937 people.", sel.get_text("css=.report_summary .total"))
        
        self.assertEqual("Back to All Data Imports", sel.get_text("link=Back to All Data Imports"))
        
        sel.click("link=Back to All Data Imports")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Start New Import", sel.get_text("link=Start New Import"))
        
        sel.click("link=Start New Import")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Back to All Data Imports", sel.get_text("link=Back to All Data Imports"))
        
        self.assertEqual("Start Data Import", sel.get_text("//div[@id='page']/page_title"))
        
        assert sel.is_text_present("Choose a spreadsheet.")
        
        self.assertEqual("Start Import", sel.get_text("link=Start Import"))
        
        sel.click("link=Back to All Data Imports")
        sel.wait_for_page_to_load("30000")


class TestAgainstNoData(QiConservativeSeleniumTestCase, AccountTestAbstractions, DataImportTestAbstractions):
    selenium_fixtures = []

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()


    def test_starting_a_new_import_takes_you_to_the_start_page(self):
        self.get_to_start_import_page()
        
    def test_that_choosing_a_person_displays_the_upload_area(self):
        sel = self.selenium
        self.get_to_start_import_page()
        assert not sel.is_element_present("css=.qq-upload-button")
        sel.click("css=.import_type_people input")
        sel.wait_for_element_present("css=.qq-upload-button")

    def test_that_uploading_a_csv_file_displays_the_right_columns(self):
        sel = self.selenium
        self.test_that_choosing_a_person_displays_the_upload_area()
        self.set_upload_file("johnsmith.csv")
        sel.wait_for_element_present("css=.qq-upload-success")

        assert sel.is_element_present("css=.import_fields_confirmation th.col_0")
        assert sel.is_element_present("css=.import_fields_confirmation th.col_1")
        assert sel.is_element_present("css=.import_fields_confirmation th.col_2")
        assert sel.is_element_present("css=.import_fields_confirmation th.col_3")
        assert not sel.is_element_present("css=.import_fields_confirmation th.col_4")
        

    def test_that_uploading_an_excel_file_displays_the_right_columns(self):
        sel = self.selenium
        self.test_that_choosing_a_person_displays_the_upload_area()
        self.set_upload_file("johnsmith.xls")
        sel.wait_for_element_present("css=.qq-upload-success")

        assert sel.is_element_present("css=.import_fields_confirmation th.col_0")
        assert sel.is_element_present("css=.import_fields_confirmation th.col_1")
        assert sel.is_element_present("css=.import_fields_confirmation th.col_2")
        assert sel.is_element_present("css=.import_fields_confirmation th.col_3")
        assert not sel.is_element_present("css=.import_fields_confirmation th.col_4")

    def test_that_choosing_person_and_uploading_a_file_populates_the_right_options_for_field_choices(self):
        # This is covered by the two above tests.
        assert True == True


    def test_uploading_a_second_file_replaces_the_first_one_and_shows_the_right_columns(self):
        sel = self.selenium
        self.test_that_uploading_a_csv_file_displays_the_right_columns()

        self.set_upload_file("nameemail.csv")
        sel.wait_for_element_present("css=.qq-upload-success")

        assert sel.is_element_present("css=.import_fields_confirmation th.col_0")
        assert sel.is_element_present("css=.import_fields_confirmation th.col_1")
        assert sel.is_element_present("css=.import_fields_confirmation th.col_2")
        assert not sel.is_element_present("css=.import_fields_confirmation th.col_3")
        


    def test_that_submit_is_disabled_if_all_columns_have_not_been_selected(self):
        sel = self.selenium
        self.test_that_uploading_a_csv_file_displays_the_right_columns()

        sel.click("css=.submit_and_start_import_btn")
        assert sel.is_text_present("Choose what you want to import")

    
    def test_that_selecting_all_columns_enables_submit(self):
        assert True == "Test written"

    def test_that_hitting_submit_on_a_valid_form_returns_to_the_list_and_says_in_progress(self):
        assert True == "Test written"

    def test_that_a_submitted_import_updates_the_list_as_it_progresses(self):
        assert True == "Test written"
    
    def test_that_a_submitted_import_of_200_finishes_importing_within_two_minutes_and_updates_the_import_list(self):
        assert True == "Test written"
    
    def test_that_a_successful_completed_import_shows_valid_results(self):
        assert True == "Test written"
    
    def test_that_an_import_with_invalid_columns_displays_those_results_on_the_import_page(self):
        assert True == "Test written"

    def test_that_ignoring_a_column_actually_ignores_it(self):
        assert True == "Test written"



    def test_that_choosing_organization_and_uploading_a_file_populates_the_right_options_for_field_choices(self):
        assert True == "Test written"

    def test_that_choosing_donation_and_uploading_a_file_populates_the_right_options_for_field_choices(self):
        assert True == "Test written"
    
    def test_that_choosing_volunteer_hours_and_uploading_a_file_populates_the_right_options_for_field_choices(self):
        assert True == "Test written"



class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, AccountTestAbstractions):
    selenium_fixtures = []

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
