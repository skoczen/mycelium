from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from picklefield.fields import PickledObjectField
from data_import.spreadsheet import Spreadsheet, IMPORT_TYPE, SPREADSHEET_SOURCE_TYPES

from accounts.models import AccountBasedModel, UserAccount
from django.core.cache import cache


class PotentiallyImportedModel(models.Model):
    old_id = models.IntegerField(blank=True, null=True, db_index=True)

    class Meta:
        abstract = True

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

