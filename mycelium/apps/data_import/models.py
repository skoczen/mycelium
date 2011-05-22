from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin
from picklefield.fields import PickledObjectField
from data_import.spreadsheet import Spreadsheet, IMPORT_ROW_TYPES, SPREADSHEET_SOURCE_TYPES, IMPORT_ROW_TYPE_TUPLES

from accounts.models import AccountBasedModel, UserAccount
from django.core.cache import cache


class PotentiallyImportedModel(models.Model):
    old_id = models.IntegerField(blank=True, null=True, db_index=True)

    class Meta:
        abstract = True

class DataImport(AccountBasedModel, TimestampModelMixin):
    importer        = models.ForeignKey(UserAccount)
    start_time      = models.DateTimeField(blank=True)
    finish_time     = models.DateTimeField(blank=True, null=True)
    import_type     = models.CharField(choices=IMPORT_ROW_TYPE_TUPLES, max_length=50)
    num_source_rows = models.IntegerField(blank=True, null=True)

    source_filename = models.TextField()
    fields          = PickledObjectField(blank=True, null=True)
    has_header      = models.BooleanField(default=False)
    results         = PickledObjectField(blank=True, null=True)


    def __unicode__(self):
        return "%s on %s" % (self.import_type, self. start_time)

    class Meta:
        ordering = ("-start_time",)

    @property
    def cache_key_prefix(self):
        return "DataImport-%s" % (self.pk)

    @property
    def cache_key_num_imported(self):
        return "%s-numimported" % (self.cache_key_prefix,)

    @classmethod
    def cache_key_for_import_id_num_imported(self, import_id):
        return "DataImport-%s-numimported" % (import_id)
    
    @classmethod
    def cache_key_for_import_id_percent_imported(self, import_id):
        return "DataImport-%s-pctimported" % (import_id)

    @classmethod
    def cache_based_percent_imported_for_import_id(cls, import_id):
        return cache.get(cls.cache_key_for_import_id_percent_imported(import_id))

    @property
    def is_started(self):
        return self.start_time != None
    
    @property
    def is_finished(self):
        return self.finish_time != None
    
    @property
    def percent_imported(self):
        if self.is_finished:
            return 100
        else:
            return cache.get(DataImport.cache_key_for_import_id_percent_imported(self.pk))

    @property
    def import_time(self):
        if self.is_finshed:
            return self.finish_time - self.start_time
        else:
            return None


    @property
    def num_columns(self):
        return len(self.fields)

    @property
    def num_new_records(self):
        pass
    
    @property
    def num_matches(self):
        pass

    @property
    def num_errors(self):
        pass