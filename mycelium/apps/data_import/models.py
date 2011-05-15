from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from picklefield.fields import PickledObjectField

from accounts.models import AccountBasedModel, UserAccount
from django.core.cache import cache

IMPORT_TYPE = [
    (0, "People"),
    (10, "Companies/Organizations"),
    (20, "Volunteer Hours"),
    (30, "Donations"),
]

SPREADSHEET_SOURCE_TYPES = [
    (0, "CSV"),
    (10, "Excel"),
]

class PotentiallyImportedModel(models.Model):
    old_id = models.IntegerField(blank=True, null=True, db_index=True)

    class Meta:
        abstract = True


class Spreadsheet:
    def __init__(self, fh):
        # fh is the file handler.
        self.file = fh
        self.parsed_spreadsheet = self._parse_file(self.file)

    # Functions to read and save a spreadsheet to the db
    def parse_file(self):
        pass

    def _save_parsed_row(self):
        pass


    # Functions to generate a spreadsheet from the db
    def generate_file(self):
        pass

    def _write_generated_row(self):
        pass

    def num_rows(self):
        pass

    def get_row(self, row_number=0):
        pass
    
    def has_header(self):
        return False
    


class ImportSpreadsheet(AccountBasedModel, TimestampModelMixin, Spreadsheet):
    source_file       = models.FileField(upload_to="import", blank=True, null=True)
    source_type       = models.IntegerField(choices=SPREADSHEET_SOURCE_TYPES, blank=True, null=True)
    columns           = PickledObjectField(blank=True, null=True)


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
    def import_result_dict(cls, success, source_row):
        return {
            'success': success,
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