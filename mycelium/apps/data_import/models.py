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

CSV_TYPE = "CSV"
EXCEL_TYPE = "EXCEL"
SPREADSHEET_SOURCE_TYPES = [
    (CSV_TYPE,   "CSV"),
    (EXCEL_TYPE, "Excel"),
]
CSV_EXTENSIONS = ["csv",]
EXCEL_EXTENSIONS = ["xls","xlsx"]

class ImportRow:
    name = None
    model = None

    def __init__(self, account, row_data_dict):
        self.account = account
        self.data = row_data_dict

    def has_sufficient_fields_for_identity(self):
        raise Exception, "Not implemented on subclassing!"
    
    def get_target_object(self):
        raise Exception, "Not implemented on subclassing!"

    def do_row_import(self):
        if self.has_sufficient_fields_for_identity():
            target = self.get_target_object()
            for k,v in self.data.iteritems():
                target.__dict__[k] = v
            
            target.save()
            return True
        else:
            return False


class PeopleImportRow(ImportRow):

    def has_sufficient_fields_for_identity(self):
        has_fields = False
        if ("first_name" in self.data and "last_name" in self.data) or \
            "email" in self.data or \
            "phone_number" in self.data:
            has_fields = True

        return has_fields
    
    def get_target_object(self):
        from people.models import Person
        if self.has_sufficient_fields_for_identity:
            # find the matching row
            q = Person.objects_by_account(self.account).all()
            if "first_name" in self.data:
                q = q.filter(first_name=self.data["first_name"])
            if "last_name" in self.data:
                q = q.filter(last_name=self.data["last_name"])

            if q.count() == 1:
                return q[0]

            q = Person.objects_by_account(self.account).all()
            if "email" in self.data:
                q = q.filter(email=self.data["email"])
            if q.count() == 1:
                return q[0]
            elif q.count() > 1:
                if "first_name" in self.data:
                    q = q.filter(first_name=self.data["first_name"])
                if "last_name" in self.data:
                    q = q.filter(last_name=self.data["last_name"])
                if q.count() == 1:
                    return q[0]
                elif q.count() > 1:
                    if "phone_number" in self.data:
                        q = q.filter(phone_number=self.data["phone_number"])
                    if q.count() == 1:
                        return q[0]


            q = Person.objects_by_account(self.account).all()
            if "phone_number" in self.data:
                q = q.filter(phone_number=self.data["phone_number"])
            if q.count() == 1:
                return q[0]
            elif q.count() > 1:
                if "first_name" in self.data:
                    q = q.filter(first_name=self.data["first_name"])
                if "last_name" in self.data:
                    q = q.filter(last_name=self.data["last_name"])
                if q.count() == 1:
                    return q[0]
            
        return Person.raw_objects.create(account=self.account)


IMPORT_ROW_TYPES = {
    'people':PeopleImportRow,
}


class PotentiallyImportedModel(models.Model):
    old_id = models.IntegerField(blank=True, null=True, db_index=True)

    class Meta:
        abstract = True


class Spreadsheet:
    def __init__(self, account, fh, import_type, filename=None):
        # fh is a file handler-like object
        self.account = account
        self.file = fh
        self.filename = filename
        self.import_type = import_type
        self.has_header = False
        self._parse_file()
        self.import_row_class = IMPORT_ROW_TYPES[import_type]

    # Functions to read and save a spreadsheet to the db
    def _parse_file(self):
        self.parsed_spreadsheet = None
        if self.type == EXCEL_TYPE:
            self.parsed_spreadsheet = self._parsed_excel()
        elif self.type == CSV_TYPE:
            self.parsed_spreadsheet = self._parsed_csv()

    @property
    def _is_valid_csv(self):
        try:
            self.file.seek(0)
            s = self.file.read(2048)
            dialect = csv.Sniffer().sniff(s)
            self.has_header = csv.Sniffer().has_header(s)
            self.file.seek(0)
            return dialect != None
        except:
            return False
    
    @property
    def _is_valid_excel(self):
        try:
            self.file.seek(0)
            self.file_contents = self.file.read()
            if not hasattr(self,"wb") or len(self.wb.sheets()) == 0:
                self.wb = xlrd.open_workbook(file_contents=self.file_contents)
                assert (len(self.wb.sheets()) > 0)
                self.has_header = False
                return True
            else:
                return True
        except:
            return False

    @property
    def is_valid(self):
        if self.type == EXCEL_TYPE:
            return self._is_valid_excel
        elif self.type == CSV_TYPE:
            return self._is_valid_csv
        else:
            return False


    def _parsed_excel(self):
        s = self.wb.sheets()[0]
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
            if self._is_valid_excel:
                file_type = EXCEL_TYPE
            elif self._is_valid_csv:
                file_type = CSV_TYPE
        else:
            # try to parse a csv first
            if self._is_valid_csv:
                file_type = CSV_TYPE
            elif self._is_valid_excel:
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
    @classmethod
    def _create_spreadsheet_excel(self, query_set, fields, file_handler=None, file_name=None):
        if not file_handler and not file_name:
            raise Exception, "Missing file handler and file name!"
        
        # silently prefer file_handler if both are passed for some reason.
        if not file_handler and file_name:
            file_handler = open(file_name, "wb")
        
        book = xlwt.Workbook()
        sheet1= book.add_sheet('Sheet 1')

        row = 0
        for r in query_set:
            col = 0
            for f in fields:
                sheet1.write(row, col, r.__dict__[f])
                col += 1
            row += 1
        
        book.save(file_handler)
        file_handler.flush()
        return file_handler

    @classmethod
    def _create_spreadsheet_csv(self, query_set, fields, file_handler=None, file_name=None):
        if not file_handler and not file_name:
            raise Exception, "Missing file handler and file name!"
        
        # silently prefer file_handler if both are passed for some reason.
        if not file_handler and file_name:
            file_handler = open(file_name, "wb")

        csv_writer = csv.writer(file_handler)
        csv_writer.writerows([r.__dict__[f] for f in fields] for r in query_set)
        file_handler.flush()
        return file_handler

    @classmethod
    def create_spreadsheet(cls, query_set, fields, file_type=CSV_TYPE, file_handler=None, file_name=None):
        if file_type == CSV_TYPE:
            return cls._create_spreadsheet_csv(query_set, fields, file_handler=file_handler, file_name=file_name)
        elif file_type == EXCEL_TYPE:
            return cls._create_spreadsheet_excel(query_set, fields, file_handler=file_handler, file_name=file_name)
        else:
            return False

    def _write_generated_row(self):
        pass

    @property
    def num_rows(self):
        return len(self.parsed_spreadsheet)

    def get_row(self, row_number=0):
        return self.parsed_spreadsheet[row_number]
    
    def get_row_dict(self, fields, row_number=0):
        d = {}
        row = self.parsed_spreadsheet[row_number]
        i = 0
        for f in fields:
            d[f] = row[i]
            i += 1
        return d
    
    def get_rows(self, start_number, end_number):
        if self.has_header:
            start_number += 1
            end_number += 1
        return [self.get_row(i) for i in range(start_number, end_number+1)]

    @property
    def header_row(self):
        if self.has_header:
            return self.parsed_spreadsheet[0]
    

    def _import_row(self, row):
        c = self.import_row_class(self.account, row)
        worked = c.do_row_import()
        return worked


    def do_import(self, fields):
        if self.is_valid:
            results = []
            for i in range(0,self.num_rows):
                row = self.get_row_dict(fields, i)
                results.append(self._import_row(row))
            return results
        else:
            raise Exception, "Invalid spreadsheet!"


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

