from celery.task import task
from data_import.models import DataImport
from data_import.spreadsheet import Spreadsheet
from accounts.models import Account
from django.core.files.storage import default_storage
import datetime

from johnny import cache as jcache

@task
def queue_data_import(acct, import_record):
    account = Account.objects.get(pk=acct.pk)
    r = DataImport.objects.get(pk=import_record.pk)

    print "Starting data import for %s" % import_record

    # Grab the spreadsheet, parse it, prep for import.
    fh = default_storage.open(r.source_filename, 'r')
    s = Spreadsheet(account, fh, r.import_type, filename=r.source_filename, cache_key_pct_complete=DataImport.cache_key_for_import_id_percent_imported(r.pk))
    r.num_source_rows = s.num_rows
    r.save()
    
    # invalidate johnny cache
    # jcache.invalidate(DataImport)

    print "Parsing complete. Starting import.."

    # Do the import
    results = s.do_import(fields=r.fields)

    print "Done, saving results."

    # Save the results
    r.results = results
    r.finish_time = datetime.datetime.now()
    r.save()

    for m in s.import_row_class(account, {}).get_target_models():
        jcache.invalidate(m)
    print "Results saved."