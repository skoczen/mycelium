from test_factory import Factory
from spreadsheets.spreadsheet import SpreadsheetAbstraction, EXCEL_TYPE, CSV_TYPE
TEST_SPREADSHEET_PATH = "apps/data_import/tests/test_spreadsheets"

class GenerateSpreadsheetsMixin:
    def _person_dict(self, person):
        return {
            'first_name': person.first_name,
            'last_name': person.last_name,
            'email': person.email,
            'phone_number': person.phone_number,
        }


    def create_people_csv_file(self, account, num_people=200):
        assert True == "Implemented"
        return None

    def create_people_excel_file(self, account, num_people=200):
        assert True == "Implemented"
        return None


    def create_organization_csv_file(self, account, num_people=200):
        assert True == "Implemented"
        return None

    def create_organization_excel_file(self, account, num_people=200):
        assert True == "Implemented"
        return None


    def create_donations_csv_file(self, account, num_people=200):
        assert True == "Implemented"
        return None

    def create_donations_excel_file(self, account, num_people=200):
        assert True == "Implemented"
        return None 



    def create_volunteers_csv_file(self, account, num_people=200):
        assert True == "Implemented"
        return None

    def create_volunteers_excel_file(self, account, num_people=200):
        assert True == "Implemented"
        return None


    def created_and_imported_csv_spreadsheet(self, **kwargs):
        fh = Factory.people_spreadsheet(self.a1, file_type=CSV_TYPE, **kwargs)

        # import it
        fh.seek(0)
        s = SpreadsheetAbstraction(self.a1, fh, "people", filename="test.csv")
        self.assertEqual(s.is_valid,True)
        return s

    def created_and_imported_excel_spreadsheet(self, **kwargs):
        fh = Factory.people_spreadsheet(self.a1, file_type=EXCEL_TYPE, **kwargs)

        # import it
        fh.seek(0)
        s = SpreadsheetAbstraction(self.a1, fh, "people", filename="test.xls")
        self.assertEqual(s.is_valid,True)
        return s