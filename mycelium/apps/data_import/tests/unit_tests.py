import time
import datetime
from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase
from groups.models import Group
from data_import.models import DataImport, Spreadsheet, ImportSpreadsheet, EXCEL_TYPE, CSV_TYPE
from data_import.tests.abstractions import GenerateSpreadsheetsMixin
from people.models import Person


class Dummy(object):
    pass

class TestModels(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase, GenerateSpreadsheetsMixin):

    def setUp(self):
        self.a1 = Factory.create_demo_site("test1", quick=True)

    def test_num_rows(self):
        # get a sample random spreadsheet with a number of rows I know
        s = self.created_and_imported_csv_spreadsheet()
        # assert that the num_rows function returns what I thought it should
        self.assertEqual(s.num_rows, Person.objects_by_account(self.a1).count())


        s2 = self.created_and_imported_excel_spreadsheet()
        # assert that the num_rows function returns what I thought it should
        self.assertEqual(s2.num_rows, Person.objects_by_account(self.a1).count())

   
    def test_get_row(self):
        s = self.created_and_imported_csv_spreadsheet(fields=["first_name","email"])
        # assert that the num_rows function returns what I thought it should
        
        p1 = Person.objects_by_account(self.a1).all()[0]
        p2 = Person.objects_by_account(self.a1).all()[2]

        self.assertEqual(s.get_row(0), [p1.first_name, p1.email])
        self.assertEqual(s.get_row(2), [p2.first_name, p2.email])
        
    
    def test_get_rows(self):
        s = self.created_and_imported_csv_spreadsheet(fields=["last_name","phone_number", "first_name"])
        # assert that the num_rows function returns what I thought it should
        
        p1 = Person.objects_by_account(self.a1).all()[0]
        p2 = Person.objects_by_account(self.a1).all()[1]
        p3 = Person.objects_by_account(self.a1).all()[2]
        people = [p1, p2, p3]

        self.assertEqual(s.get_rows(0,2), [[p.last_name, p.phone_number, p.first_name,] for p in people ])
        


    def test__detect_type(self):
        fh = Factory.people_spreadsheet(self.a1, file_type=CSV_TYPE)
        s = Spreadsheet(self.a1, fh, "people", filename="test.foo")
        self.assertEqual(s.type, CSV_TYPE)
        self.assertEqual(s.is_valid,True)
        

        fh = Factory.people_spreadsheet(self.a1, file_type=EXCEL_TYPE)
        s = Spreadsheet(self.a1, fh, "people", filename="test.bar")
        self.assertEqual(s.type, EXCEL_TYPE)
        self.assertEqual(s.is_valid,True)



class TestDataImport(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase, GenerateSpreadsheetsMixin):

    def setUp(self):
        self.a1 = Factory.create_demo_site("test1", quick=True)
        pass
   
    def _that_importing_a_person_spreadsheet_refills_an_emptied_database(self, file_type, extension):
        # create a bunch of people
        # store their info in a dict
        people_info = [self._person_dict(p) for p in Person.objects_by_account(self.a1)]

        # create a person spreadsheet
        fh = Factory.people_spreadsheet(self.a1, file_type=file_type)

        # delete all the people
        Person.objects_by_account(self.a1).all().delete()

        # assert that they're gone
        self.assertEqual(Person.objects_by_account(self.a1).count(), 0)

        # import the spreadsheet
        s = Spreadsheet(self.a1, fh, "people", filename="test.%s" % (extension,))
        s.do_import(fields=["first_name","last_name","email","phone_number"])

        # assert that they're back.
        people_info2 = [self._person_dict(p) for p in Person.objects_by_account(self.a1)]

        self.assertEqual(people_info, people_info2)


    def test_that_importing_a_person_csv_refills_an_emptied_database(self):
        return self._that_importing_a_person_spreadsheet_refills_an_emptied_database(CSV_TYPE,"csv")

    def test_that_importing_an_person_excel_refills_an_emptied_database(self):
        return self._that_importing_a_person_spreadsheet_refills_an_emptied_database(EXCEL_TYPE,"xls")



    def test_that_importing_a_organization_csv_works(self):
        assert True == "Test Written"

    def test_that_importing_a_organization_excel_works(self):
        assert True == "Test Written"


    def test_that_importing_a_donations_csv_works(self):
        assert True == "Test Written"

    def test_that_importing_a_donations_excel_works(self):
        assert True == "Test Written"

    def test_that_importing_a_volunteers_csv_works(self):
        assert True == "Test Written"

    def test_that_importing_a_volunteers_excel_works(self):
        assert True == "Test Written"
    
    
    def test_ignoring_a_column_actually_ignores_it(self):
        assert True == "Test Written"

    def test_that_a_blank_row_is_ignored(self):
        assert True == "Test Written"

    def test_importing_a_spreadsheet_with_an_invalid_person_row_ignores_the_row_and_finishes_properly(self):
        assert True == "Test Written"

    def test_that_importing_a_csv_and_an_excel_file_with_identical_data_produce_an_identical_spreadsheet_object(self):
        assert True == "Test Written"
    
    def test_importing_a_first_name_works(self):
        assert True == "Test Written"

    def test_importing_a_full_name_works(self):
        assert True == "Test Written"

    def test_importing_a_last_name_works(self):
        assert True == "Test Written"

    def test_importing_an_email_works(self):
        assert True == "Test Written"

    def test_importing_a_phone_number_works(self):
        assert True == "Test Written"

    def test_importing_a_full_block_address_works(self):
        assert True == "Test Written"
    
    def test_importing_an_address_line_one_works(self):
        assert True == "Test Written"

    def test_importing_an_address_line_two_works(self):
        assert True == "Test Written"

    def test_importing_a_city_works(self):
        assert True == "Test Written"

    def test_importing_a_state_works(self):
        assert True == "Test Written"

    def test_importing_a_zip_works(self):
        assert True == "Test Written"


    def test_importing_a_work_company_name_works(self):
        assert True == "Test Written"

    def test_importing_a_work_email_works(self):
        assert True == "Test Written"

    def test_importing_a_work_phone_number_works(self):
        assert True == "Test Written"

    def test_importing_a_work_full_block_address_works(self):
        assert True == "Test Written"
    
    def test_importing_a_work_address_line_one_works(self):
        assert True == "Test Written"

    def test_importing_a_work_address_line_two_works(self):
        assert True == "Test Written"

    def test_importing_a_work_city_works(self):
        assert True == "Test Written"

    def test_importing_a_work_state_works(self):
        assert True == "Test Written"

    def test_importing_a_work_zip_works(self):
        assert True == "Test Written"


    


    def test_that_importing_a_volunteer_shift_works(self):
        assert True == "Test Written"

    def test_that_importing_volunteer_status_works(self):
        assert True == "Test Written"

    def test_that_importing_a_donation_works(self):
        assert True == "Test Written"

    def test_that_importing_and_creating_tags_from_separate_columns_works(self):
        assert True == "Test Written"

    def test_that_importing_and_creating_tags_from_one_comma_separated_column_works(self):
        assert True == "Test Written"

    def test_that_importing_existing_tags_from_separate_columns_works(self):
        assert True == "Test Written"

    def test_that_importing_existing_tags_from_one_comma_separated_column_works(self):
        assert True == "Test Written"




    def test_that_importing_the_same_spreadsheet_multiple_times_is_idempotent(self):
        assert True == "Test Written"

    def test_that_importing_a_spreadsheet_over_modified_fields_overwrites_them(self):
        """Test with first name, email, phone number, address two, 
           (if appropriate) donation amount, donation date, vol shift hours, and vol shift date"""
        assert True == "Test Written"

    def test_that_importing_a_modified_spreadsheet_over_existing_fields_overwrites_them(self):
        """Test with first name, email, phone number, address two, 
           (if appropriate) donation amount, donation date, vol shift hours, and vol shift date"""
        assert True == "Test Written"
    


    def test_identity_tests_written(self):
        assert True == "Test Written"


    def test_write_around_style_file_works(self):
        assert True == "Test Written"

    def test_tom_style_file_works(self):
        assert True == "Test Written"
    
    def test_st_gerard_style_file_works(self):
        assert True == "Test Written"


class TestSpreadsheetGenerations(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase, GenerateSpreadsheetsMixin):
    
    def test_that_creating_a_person_csv_succeeds(self):
        assert True == "Test Written"

    def test_that_creating_a_person_excel_succeeds(self):
        assert True == "Test Written"


    def test_that_creating_a_organization_csv_succeeds(self):
        assert True == "Test Written"

    def test_that_creating_a_organization_excel_succeeds(self):
        assert True == "Test Written"


    def test_that_creating_a_donations_csv_succeeds(self):
        assert True == "Test Written"

    def test_that_creating_a_donations_excel_succeeds(self):
        assert True == "Test Written"

    def test_that_creating_a_volunteers_csv_succeeds(self):
        assert True == "Test Written"

    def test_that_creating_a_volunteers_excel_succeeds(self):
        assert True == "Test Written"


class TestSpreadSheetGenerationLoop(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase, GenerateSpreadsheetsMixin):

    def test_that_creating_a_person_csv_then_importing_it_leaves_the_same_data(self):
        assert True == "Test Written"

    def test_that_creating_a_person_excel_then_importing_it_leaves_the_same_data(self):
        assert True == "Test Written"


    def test_that_creating_a_organization_csv_then_importing_it_leaves_the_same_data(self):
        assert True == "Test Written"

    def test_that_creating_a_organization_excel_then_importing_it_leaves_the_same_data(self):
        assert True == "Test Written"


    def test_that_creating_a_donations_csv_then_importing_it_leaves_the_same_data(self):
        assert True == "Test Written"

    def test_that_creating_a_donations_excel_then_importing_it_leaves_the_same_data(self):
        assert True == "Test Written"



    def test_that_creating_a_volunteers_csv_then_importing_it_leaves_the_same_data(self):
        assert True == "Test Written"

    def test_that_creating_a_volunteers_excel_then_importing_it_leaves_the_same_data(self):
        assert True == "Test Written"