from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from picklefield.fields import PickledObjectField
import csv
import xlwt
import xlrd

from accounts.models import AccountBasedModel, UserAccount
from django.core.cache import cache

IMPORT_TYPE = [
    (0, "People"),
    (10, "Companies/Organizations"),
    (20, "Volunteer Hours"),
    (30, "Donations"),
]

CSV_TYPE = 10
EXCEL_TYPE = 20
SPREADSHEET_SOURCE_TYPES = [
    (CSV_TYPE,   "CSV"),
    (EXCEL_TYPE, "Excel"),
]
CSV_EXTENSIONS = ["csv",]
EXCEL_EXTENSIONS = ["xls","xlsx"]


class PotentiallyImportedModel(models.Model):
    old_id = models.IntegerField(blank=True, null=True, db_index=True)

    class Meta:
        abstract = True


class Spreadsheet:
    def __init__(self, fh, filename=None):
        # fh is a file handler-like object
        self.file = fh
        self.filename = filename
        self.has_header = False
        self._parse_file()

    # Functions to read and save a spreadsheet to the db
    def _parse_file(self):
        self.parsed_spreadsheet = None
        if self.type == EXCEL_TYPE:
            self.parsed_spreadsheet = self._parsed_excel()
        elif self.type == CSV_TYPE:
            self.parsed_spreadsheet = self._parsed_csv()

    @property
    def is_valid_csv(self):
        try:
            s = self.file.read(2048)
            dialect = csv.Sniffer().sniff(s)
            self.has_header = csv.Sniffer().has_header(s)
            self.file.seek(0)
            return dialect != None
        except:
            return False
    
    @property
    def is_valid_excel(self):
        try:
            self.file_contents = self.file.read()
            wb = xlrd.open_workbook(file_contents=self.file_contents)
            assert len(wb.sheets()) > 0
            self.has_header = False
            return True
        except:
            return False

    def _parsed_excel(self):
        wb = xlrd.open_workbook(file_contents=self.file_contents)
        s = wb.sheets()[0]
        # get the value for each cell for each row in all rows
        return [[cell.value for cell in s.row(i)] for i in range(0,s.nrows)]

    def _parsed_csv(self):
        return [r for r in csv.reader(self.file)]


    def _detect_type(self):
        probable_type = None
        if self.filename:
            extension = self.filename[self.filename.rfind(".")+1:]

            if extension in CSV_EXTENSIONS:
                probable_type = CSV_TYPE
            elif extension in EXCEL_EXTENSIONS:
                probable_type = EXCEL_TYPE
        
        file_type = None
        if probable_type and probable_type == EXCEL_TYPE:
            # try to parse an excel file first
            if self.is_valid_excel:
                file_type = EXCEL_TYPE
            elif self.is_valid_csv:
                file_type = CSV_TYPE
        else:
            # try to parse a csv first
            if self.is_valid_csv:
                file_type = CSV_TYPE
            elif self.is_valid_excel:
                file_type = EXCEL_TYPE
        
        return file_type
    
    @property
    def type(self):
        if not hasattr(self,"cached_type"):
            self.cached_type = self._detect_type()
        return self.cached_type

    def _save_parsed_row(self):
        pass


    # Functions to generate a spreadsheet from the db
    def generate_file(self):
        pass

    def _write_generated_row(self):
        pass

    @property
    def num_rows(self):
        return len(self.parsed_spreadsheet)

    def get_row(self, row_number=0):
        return self.parsed_spreadsheet[row_number]
    
    def get_rows(self, start_number, end_number):
        if self.has_header:
            start_number += 1
            end_number += 1
        return [self.get_row(i) for i in range(start_number, end_number)]

    @property
    def header_row(self):
        if self.has_header:
            return self.parsed_spreadsheet[0]
    


class ImportSpreadsheet(AccountBasedModel, TimestampModelMixin, Spreadsheet):
    source_file       = models.FileField(upload_to="import", blank=True, null=True)
    source_type       = models.IntegerField(choices=SPREADSHEET_SOURCE_TYPES, blank=True, null=True)
    columns           = PickledObjectField(blank=True, null=True)
    has_header        = models.BooleanField(default=False)


class DataImport(AccountBasedModel, TimestampModelMixin):
    importer        = models.ForeignKey(UserAccount)
    start_time      = models.DateTimeField(blank=True)
    finish_time     = models.DateTimeField(blank=True, null=True)
    import_type     = models.IntegerField(choices=IMPORT_TYPE)
    num_source_rows = models.IntegerField(blank=True, null=True)
    spreadsheet     = models.ForeignKey(ImportSpreadsheet)

    @property
    def cache_key_prefix(self):
        return "DataImport-%s" % (self.pk)

    @property
    def cache_key_num_imported(self):
        return "%s-numimported" % (self.cache_key_prefix,)

    @property
    def is_started(self):
        return True
    
    @property
    def is_finished(self):
        return self.finish_time != None
    
    @property
    def percent_imported(self):
        if self.is_finished:
            return 100
        else:
            num_imported = cache.get(self.cache_key_num_imported, 1)
            return num_imported / self.spreadsheet.num_rows

    @property
    def import_time(self):
        if self.is_finshed:
            return self.finish_time - self.start_time
        else:
            return None

    @classmethod
    def import_result_dict(cls, success, number, obj, source_row, error_message=""):
        # potentially do some smart things here, instead of just **kwargs.
        return {
            'success': success,
            'error_message': error_message,
            'number': number,
            'obj': obj,
            'source_row': source_row
        }



# class SpreadsheetColumn(models.Model):
#     spreadsheet = models.ForeignKey(Spreadsheet)
#     heading     = models.CharField(blank=True, null=True, max_length=255)  # "First Name"
#     model_type  = models.CharField(blank=True, null=True, max_length=255)  # "people.Person"
#     model_field = models.CharField(blank=True, null=True, max_length=255)  # "first_name"


#     class Meta:
#         abtract = True

#     def string_to_python(self, str):
#         pass

#     def python_to_string(self, str):
#         pass


# class SpreadsheetRow(models.Model):
#     spreadsheet = models.ForeignKey(Spreadsheet)

#     class Meta:
#         abtract = True
    
#     @property
#     def objects(self):
#         return self._objects
    
#     def create_objects(self):
#         self._objects = []

#     def save_objects(self):
#         for o in self.objects:
#             o.save()

# class ImportSpreadsheetColumn(AccountBasedModel, TimestampModelMixin, SpreadsheetColumn):
#     pass

# class ImportSpreadsheetRow(AccountBasedModel, TimestampModelMixin, SpreadsheetRow):
#     pass