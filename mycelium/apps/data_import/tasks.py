from celery.task import task
from data_import.models import DataImport, ResultsRow
from spreadsheets.spreadsheet import SpreadsheetAbstraction
from accounts.models import Account
from django.core.files.storage import default_storage
import datetime

from johnny import cache as jcache
from django.core.cache import cache

@task
def queue_data_import(acct_id, import_record):
    account = Account.objects.get(pk=acct_id)
    r = DataImport.raw_objects.get(pk=import_record.pk)

    # print "Starting data import for %s" % import_record

    try:

        # Grab the spreadsheet, parse it, prep for import.
        fh = default_storage.open(r.source_filename, 'r')
        s = SpreadsheetAbstraction(account, fh, r.import_type, filename=r.source_filename, cache_key_pct_complete=DataImport.cache_key_for_import_id_percent_imported(r.pk))
        r.num_source_rows = s.num_rows
        r.save()
        
        # invalidate johnny cache
        # jcache.invalidate(DataImport)

        # print "Parsing complete. Starting import.."

        # Do the import
        results = s.do_import(fields=r.fields)
        cache.set(DataImport.cache_key_for_import_id_percent_imported(r.pk),99)
        # print "Done, saving results."

        # Save the results
        for row in results:
            model_key = [v.model_key for k,v in s.import_row_class.importable_fields.items()][0]
            ResultsRow.objects.create(
                account=account,
                data_import=r,
                successfully_imported=row["success"],
                new_record_created=row["created"],
                targets=row["targets"],
                primary_target_id=row["targets"][model_key].id,  # TODO: this breaks when we go to multiple models
            )

        r.finish_time = datetime.datetime.now()
        cache.delete(DataImport.cache_key_for_import_id_percent_imported(r.pk))
        r.save()


        for m in r.import_row_class_instance.get_target_models():
            jcache.invalidate(m)
        # print "Results saved."
    except:
        r.failed = True
        r.save()