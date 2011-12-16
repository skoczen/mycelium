import logging
import csv
import xlwt
import xlrd
from collections import OrderedDict
from qi_toolkit.helpers import exception_string

from django.db.models import get_model
from django.core.cache import cache

CSV_TYPE = "CSV"
EXCEL_TYPE = "EXCEL"
SPREADSHEET_SOURCE_TYPES = [
    (CSV_TYPE,   "CSV"),
    (EXCEL_TYPE, "Microsoft Excel"),
]
CSV_EXTENSIONS = ["csv",]
EXCEL_EXTENSIONS = ["xls","xlsx"]
IGNORE_FIELD_STRING = "ignore"

log = logging.getLogger(__file__)

class SpreadsheetRow(object):
    name = None
    model = None
    fields = {}

    def __init__(self, account, row_data_dict=None, *args, **kwargs):
        self.account = account
        self.data = row_data_dict
        self.target_models = self.get_target_models()
        super(SpreadsheetRow, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.name
    

    def has_sufficient_fields_for_identity(self):
        has_fields = False
        for k,i_set in self.identity_sets.iteritems():
            # TODO: this may need split out.
            if all(f.field_getter in self.data for f in i_set):
                has_fields = True
                break
        return has_fields
    
    def get_target_models(self):
        targets = {}
        for k,v in self.fields.iteritems():
            if not v.model_key in targets:
                targets[v.model_key] = get_model(v.app, v.model)
        
        return targets
    
    def get_target_objects(self):
        targets = {}
        created = False
        for k,field in self.fields.iteritems():
            if not field.model_key in targets:
                targets[field.model_key], created = getattr(self,"get_target_object_%s" % field.model_key)()

        return targets, created

    @property
    def identity_sets(self):
        """
        Returns a dict as follows:
        {
            1: [FirstNameImportField, LastNameImportField],
            2: [EmailImportField]
        }
        """
        if not hasattr(self,"_identity_sets"):
            sets = {}
            for k,field in self.fields.iteritems():
                for i in field.identity_set:
                    if not i in sets:
                        sets[i] = []
                    if not field in sets[i]:
                        sets[i].append(field)

            self._identity_sets = sets
        return self._identity_sets

    def do_row_import(self):
        if self.has_sufficient_fields_for_identity():
            targets, created = self.get_target_objects()
            for k,v in self.data.iteritems():
                # get the ImportField obj
                f = self.fields[k]

                # set the field on the target model to the value.
                if hasattr(getattr(targets[f.model_key],f.field_setter), "__call__"):
                    getattr(targets[f.model_key],f.field_setter)(v)
                else:
                    targets[f.model_key].__dict__[f.field_setter] = v

            for k,target in targets.iteritems():
                target.save()
            
            return True, created, targets
        else:
            return False, False, []


class ImportField:
    def __init__(self, name, app, model, field_getter, field_setter=None, identity_set=[]):
        self.name = name
        self.app = app
        self.model = model
        self.field_getter = field_getter
        self.field_setter = field_setter
        self.identity_set = identity_set
    
    @property
    def model_key(self):
        return "%s_%s" % (self.app, self.model)
    
        

class PeopleImportRow(SpreadsheetRow):
    NAME_IDENTITY = "NAMES"
    EMAIL_IDENTITY = "EMAIL"
    PHONE_IDENTITY = "PHONE"


    fields =  OrderedDict([
            ('first_name',   ImportField("First Name",       "people", "Person",    "first_name",       "first_name",       identity_set=[NAME_IDENTITY,]) ),
            ('last_name',    ImportField("Last Name",        "people", "Person",    "last_name",        "last_name",        identity_set=[NAME_IDENTITY,]) ),
            ('email',        ImportField("Email",            "people", "Person",    "get_email",        "set_email",        identity_set=[EMAIL_IDENTITY,]) ),
            ('phone_number', ImportField("Phone",            "people", "Person",    "get_phone_number", "set_phone_number", identity_set=[PHONE_IDENTITY,]) ),
            ('line_1',       ImportField("Address Line 1",   "people", "Person",    "line_1",           "line_1",           identity_set=[],)               ),
            ('line_2',       ImportField("Address Line 2",   "people", "Person",    "line_2",           "line_2",           identity_set=[],)               ),
            ('city',         ImportField("City",             "people", "Person",    "city",             "city",             identity_set=[],)               ),
            ('state',        ImportField("State/Province",   "people", "Person",    "state",            "state",            identity_set=[],)               ),
            ('postal_code',  ImportField("Zip Code",         "people", "Person",    "postal_code",      "postal_code",      identity_set=[],)               ),
    ])

    def get_primary_target_model(self):
        from people.models import Person
        return Person
    
    def get_object_for_primary_target_from_id(self, id):
        from people.models import Person
        return Person.raw_objects.get(pk=id)

    def get_target_object_people_Person(self):
        from people.models import Person
        if self.has_sufficient_fields_for_identity:
            # find the matching row
            if "first_name" in self.data and "last_name" in self.data and ( self.data["first_name"] != "" or self.data["last_name"] != ""):
                q = Person.objects_by_account(self.account).all()
                if "first_name" in self.data:
                    q = q.filter(first_name=self.data["first_name"])
                if "last_name" in self.data:
                    q = q.filter(last_name=self.data["last_name"])

                if q.count() == 1:
                    return q[0], False

            # TODO: This is not ok to be commmented out. Need to figure it out.
            # # First and last name were not enough
            # q = Person.objects_by_account(self.account).all()
            # if "email" in self.data and self.data["email"] != "":
            #     q = q.filter(email=self.data["email"])
                
            #     if q.count() == 1:
            #         return q[0], False
            #     elif q.count() > 1:
            #         if "first_name" in self.data:
            #             q = q.filter(first_name=self.data["first_name"])
            #         if "last_name" in self.data:
            #             q = q.filter(last_name=self.data["last_name"])
            #         if q.count() == 1:
            #             return q[0], False
            #         elif q.count() > 1:
            #             if "phone_number" in self.data:
            #                 q = q.filter(phone_number=self.data["phone_number"])
            #             if q.count() == 1:
            #                 return q[0], False

            # # Email-based search wasn't enough

            # q = Person.objects_by_account(self.account).all()
            # if "phone_number" in self.data and self.data["phone_number"] != "":
            #     q = q.filter(phone_number=self.data["phone_number"])
            #     if q.count() == 1:
            #         return q[0], False
            #     elif q.count() > 1:
            #         if "first_name" in self.data:
            #             q = q.filter(first_name=self.data["first_name"])
            #         if "last_name" in self.data:
            #             q = q.filter(last_name=self.data["last_name"])
            #         if q.count() == 1:
            #             return q[0], False
            
            # Phone-based search wasn't enough.
        return Person.raw_objects.create(account=self.account), True


IMPORT_ROW_TYPES = {
    'people':PeopleImportRow,
}
IMPORT_ROW_TYPE_TUPLES = [(k,v) for k,v in IMPORT_ROW_TYPES.iteritems()]


class SpreadsheetAbstraction:
    def __init__(self, account, fh, import_type, filename=None, cache_key_pct_complete=""):
        # fh is a file handler-like object
        self.account = account
        self.file = fh
        self.filename = filename
        self.import_type = import_type
        self.has_header = False
        self._parse_file()
        self.import_row_class = IMPORT_ROW_TYPES[import_type]
        self.cache_key_pct_complete = cache_key_pct_complete

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
            dialect = csv.Sniffer().sniff(s, delimiters=',')
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
            extension = self.filename[self.filename.rfind(".")+1:].lower()

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

    @classmethod
    def _value_rows_from_queryset(cls, query_set, template, with_header=True,**kwargs):
        from spreadsheets.models import Spreadsheet
        rows = []

        template_instance = Spreadsheet.spreadsheet_template_instance_class(template.template_type)(query_set[0].account)
        if with_header:
            rows.append([f[1].name for f in template_instance.fields.iteritems()])
        
        for r in query_set:
            try:
                row = []
                template_instance.get_primary_target(r.account, r.pk, force_refresh=True)
                target_objects,created = template_instance.get_target_objects()

                for k,f in template.fields.iteritems():
                    col_val = None
                    if target_objects[f.model_key]:
                        # try:
                        if f.field_getter in target_objects[f.model_key].__dict__:
                            col_val = target_objects[f.model_key].__dict__[f.field_getter]
                        else:
                            col_val = eval("target_objects[f.model_key].%s" % f.field_getter)
                        # except:
                        #     row.append("")    
                    if not col_val:
                        col_val = ""
                    row.append(col_val)

                rows.append(row)
            except:
                log.warn("Error exporting row %s %s %s\n %s" % (r, r.pk, template_instance, exception_string()))
                pass

        return rows

    # Functions to generate a spreadsheet from the db
    @classmethod
    def _create_spreadsheet_excel(cls, query_set, template, file_handler=None, file_name=None, **kwargs):
        if not file_handler and not file_name:
            raise Exception, "Missing file handler and file name!"
        
        # silently prefer file_handler if both are passed for some reason.
        if not file_handler and file_name:
            file_handler = open(file_name, "wb")
        
        book = xlwt.Workbook()
        sheet1= book.add_sheet('Sheet 1')

        row = 0
        if query_set.count() > 0:
            for r in cls._value_rows_from_queryset(query_set, template, **kwargs):
                col = 0
                for c in r:
                    sheet1.write(row, col, "%s" % c)
                    col += 1
                row += 1
        
        book.save(file_handler)
        file_handler.flush()
        return file_handler

    @classmethod
    def _create_spreadsheet_csv(cls, query_set, template, file_handler=None, file_name=None,**kwargs):
        if not file_handler and not file_name:
            raise Exception, "Missing file handler and file name!"
        
        # silently prefer file_handler if both are passed for some reason.
        if not file_handler and file_name:
            file_handler = open(file_name, "wb")

        csv_writer = csv.writer(file_handler)
        if query_set.count() > 0:
            csv_writer.writerows( [unicode(c).encode("ascii","ignore") for c in r] for r in cls._value_rows_from_queryset(query_set, template, **kwargs) )
        file_handler.flush()
        return file_handler

    @classmethod
    def create_spreadsheet(cls, query_set, template, file_type=CSV_TYPE, file_handler=None, file_name=None,  **kwargs):
        if file_type == CSV_TYPE:
            return cls._create_spreadsheet_csv(query_set, template, file_handler=file_handler, file_name=file_name,  **kwargs)
        elif file_type == EXCEL_TYPE:
            return cls._create_spreadsheet_excel(query_set, template, file_handler=file_handler, file_name=file_name,  **kwargs)
        else:
            return False

    @classmethod
    def mime_type_from_file_type(cls, file_type):
        if file_type == CSV_TYPE:
            return "text/csv"
        elif file_type == EXCEL_TYPE:
            return "application/vnd.ms-excel"
        else:
            return None
    
    @classmethod
    def extension_from_file_type(cls, file_type):
        if file_type == CSV_TYPE:
            return CSV_EXTENSIONS[0]
        elif file_type == EXCEL_TYPE:
            return EXCEL_EXTENSIONS[0]
        else:
            return ""

    def _write_generated_row(self):
        pass

    @property
    def num_rows(self):
        if self.parsed_spreadsheet:
            return len(self.parsed_spreadsheet)
        else:
            return 0

    def get_row(self, row_number=0):
        return self.parsed_spreadsheet[row_number]
    
    def get_row_dict(self, fields, row_number=0):
        d = {}
        row = self.parsed_spreadsheet[row_number]
        i = 0
        for f in fields:
            if f != "" and f != IGNORE_FIELD_STRING:
                try:
                    d[f] = row[i].encode('utf-8','replace')
                except Exception, e:
                    log.warn(e)
                    d[f] = None
            i += 1
        return d
    
    def get_rows(self, start_number, end_number):
        if self.has_header:
            start_number += 1
            end_number += 1
        
        if end_number > self.num_rows:
            end_number = self.num_rows

        return [self.get_row(i) for i in range(start_number, end_number)]

    @property
    def header_row(self):
        if self.has_header:
            return self.parsed_spreadsheet[0]
    

    def _import_row(self, row):
        c = self.import_row_class(self.account, row)
        worked, created, targets = c.do_row_import()

        return {
            'success':worked,
            'created':created,
            'targets':targets,
        }


    def do_import(self, fields):
        if self.is_valid:
            results = []
            for i in range(0,self.num_rows):
                row = self.get_row_dict(fields, i)
                results.append(self._import_row(row))
                try:
                    cache.set(self.cache_key_pct_complete, int(round((100*float(i))/float(self.num_rows))))
                except:
                    pass
            try:
                cache.set(self.cache_key_pct_complete, "100")
            except:
                pass
            return results
        else:
            raise Exception, "Invalid spreadsheet!"
