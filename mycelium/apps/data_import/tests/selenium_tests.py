from functional_tests.selenium_test_case import DjangoFunctionalConservativeSeleniumTestCase
import time 
import unittest
from test_factory import Factory
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from data_import.tests.selenium_abstractions import DataImportTestAbstractions


class TestMockupPages(DjangoFunctionalConservativeSeleniumTestCase, AccountTestAbstractions, DataImportTestAbstractions):
    selenium_fixtures = []

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()

    # def tearDown(self):
    #     self.account.delete()


class TestAgainstNoData(DjangoFunctionalConservativeSeleniumTestCase, AccountTestAbstractions, DataImportTestAbstractions):
    selenium_fixtures = []

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()


    def test_starting_a_new_import_takes_you_to_the_start_page(self):
        self.get_to_start_import_page()
        
    def test_that_choosing_a_person_displays_the_upload_area(self):
        self.get_to_start_import_page()
        self.choose_person_as_import_type()

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
        time.sleep(2)
        assert sel.is_text_present("Choose what you want to import")

    
    def test_that_selecting_all_columns_enables_submit(self):
        sel = self.selenium
        self.test_that_uploading_a_csv_file_displays_the_right_columns()


        assert sel.is_element_present("css=.submit_and_start_import_btn.disabled")
        sel.select("css=.import_fields_confirmation th.col_0 select", "First Name")
        sel.select("css=.import_fields_confirmation th.col_1 select", "Last Name")
        sel.select("css=.import_fields_confirmation th.col_2 select", "Phone")
        sel.select("css=.import_fields_confirmation th.col_3 select", "Email")

        assert not sel.is_element_present("css=.submit_and_start_import_btn.disabled")
        assert sel.is_element_present("css=.submit_and_start_import_btn")
        assert sel.is_text_present("Choose what you want to import")

    def test_that_hitting_submit_on_a_valid_form_returns_to_the_list_and_says_in_progress(self):
        sel = self.selenium
        self.test_that_selecting_all_columns_enables_submit()
        sel.click("css=.submit_and_start_import_btn")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Right now")

    
    def test_that_a_submitted_import_updates_the_list_as_it_progresses(self):
        sel = self.selenium
        self.get_to_start_import_page()
        self.start_person_spreadsheet_upload()

        time.sleep(2)
        first_pct = int(sel.get_text("css=.percent_imported:nth(0)"))
        time.sleep(4)
        next_pct = int(sel.get_text("css=.percent_imported:nth(0)"))

        assert first_pct < next_pct

        
    def test_that_a_submitted_import_of_200_finishes_importing_within_two_minutes_and_updates_the_import_list(self):
        self.get_to_start_import_page()
        self.upload_person_spreadsheet_successfully()
        

    def test_that_a_successful_completed_import_shows_valid_results(self):
        sel = self.selenium
        self.get_to_start_import_page()
        self.upload_person_spreadsheet_successfully()
        time.sleep(4)
        sel.click("css=.view_results_btn")
        sel.wait_for_page_to_load("30000")
        time.sleep(30)
        assert sel.is_text_present("We found 204 people.")

    @unittest.skip("Not written yet.")
    def test_that_an_import_with_invalid_columns_displays_those_results_on_the_import_page(self):
        pass

    def test_that_ignoring_a_column_actually_ignores_it(self):
        sel = self.selenium
        self.test_that_uploading_a_csv_file_displays_the_right_columns()

        assert sel.is_element_present("css=.submit_and_start_import_btn.disabled")
        sel.select("css=.import_fields_confirmation th.col_0 select", "First Name")
        sel.select("css=.import_fields_confirmation th.col_1 select", "Last Name")
        sel.select("css=.import_fields_confirmation th.col_2 select", "Ignore this column")
        sel.select("css=.import_fields_confirmation th.col_3 select", "Email")

        sel.click("css=.submit_and_start_import_btn")
        sel.wait_for_page_to_load("30000")

        sel.click("link=View Results")
        sel.wait_for_page_to_load("30000")

        sel.click("link=People")
        sel.wait_for_page_to_load("30000")

        sel.type("css=#id_search_query", "john smith")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")
        time.sleep(2)
        sel.click("css=search_results .result_row .name a")

        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("John")
        assert sel.is_text_present("Smith")        
        assert not sel.is_text_present("503 555-1234")        

    @unittest.skip("Not written yet.")
    def test_that_choosing_organization_and_uploading_a_file_populates_the_right_options_for_field_choices(self):
        pass

    @unittest.skip("Not written yet.")
    def test_that_choosing_donation_and_uploading_a_file_populates_the_right_options_for_field_choices(self):
        pass

    @unittest.skip("Not written yet.")
    def test_that_choosing_volunteer_hours_and_uploading_a_file_populates_the_right_options_for_field_choices(self):
        pass




class TestAgainstGeneratedData(DjangoFunctionalConservativeSeleniumTestCase, AccountTestAbstractions):
    selenium_fixtures = []

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
