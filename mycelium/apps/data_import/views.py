from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.middleware.csrf import get_token
from ajaxuploader.views import AjaxFileUploader
from django.core.files.storage import default_storage

from data_import.spreadsheet import IMPORT_ROW_TYPES, IGNORE_FIELD_STRING
from data_import.models import Spreadsheet, DataImport
from data_import.tasks import queue_data_import

import datetime

@render_to("data_import/list.html")
def list(request):
    section = "more"
    all_imports = DataImport.objects_by_account(request.account).all()
    return locals()

@render_to("data_import/start.html")
def start(request):
    # TODO: this is obnoxious.  Fix it.
    section = "more"
    csrf_token = get_token( request )

    return locals()

def begin_import(request):
    if request.method == "POST":
        import_type = request.POST["upload_type"]
        filename = request.POST["upload_filename"]
        fields = []
        has_header = False

        for k,v in sorted(request.POST.iteritems()):
            if "import_col_" in k:
                fields.append(v)

        import_record = DataImport.objects.create(
            account=request.account,
            importer=request.useraccount,
            start_time=datetime.datetime.now(),
            import_type=import_type,
            source_filename=filename,
            fields=fields,
            has_header=has_header,
        )
        import_record.save()
        queue_data_import.delay(request.account.pk, import_record=import_record)
        return HttpResponseRedirect(reverse("data_import:list",))
    else:
        return HttpResponseRedirect(reverse("data_import:start",))

@json_view
def import_status(request):
    try:
        import_id = request.POST["import_id"]
        percent_imported = "%s" % DataImport.percent_imported_for_import_id(import_id)
        return {
            'success':True,
            'percent_imported': percent_imported,
            'is_finished': percent_imported == "100",
            'import_id':import_id,
        }

    except Exception, e:
        print e
        return {'success': False}

@render_to("data_import/review.html")
def review(request, import_id):
    # TODO: this is obnoxious.  Fix it.
    section = "more"
    data_import = DataImport.objects_by_account(request.account).get(pk=import_id)
    return locals()

@render_to("data_import/column_headers.js")
def import_column_headers_js(request):
    ignore_string = IGNORE_FIELD_STRING

    import_row_types = { k: v(request.account,{}) for k,v in IMPORT_ROW_TYPES.items() }
        
    return locals()

class DataImportAjaxFileUploader(AjaxFileUploader):
    def __call__(self,request, import_type):
        self.import_type = import_type
        return self._ajax_upload(request)

    def _update_filename(self, request, filename):
        import time
        return "import/%s/%s.%s" % (request.account.pk, int(time.time()), filename, )

    def _upload_complete(self, request, filename, **kwargs):
        # filename is a file at s3.  Get it.
        f = default_storage.open(filename, 'r')

        # parse the file.
        s = Spreadsheet(request.account, f, self.import_type, filename=filename)
        f.close()
        
        # get the number of rows
        num_rows = s.num_rows

        # see if it has a header
        header_row = []
        has_header = s.has_header
        if s.has_header:
            header_row = s.header_row
        
        # get the first five columns
        first_rows = s.get_rows(0,8)

        return_dict = {
            'num_rows': num_rows,
            'first_rows': first_rows,
            'header_row': header_row,
            'has_header': has_header,
            'filename':filename,
        }

        return return_dict

data_import_uploader = DataImportAjaxFileUploader()