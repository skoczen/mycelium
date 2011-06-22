from ajaxuploader.backends.s3 import S3UploadBackend
from django.core.files.storage import default_storage
from spreadsheets.spreadsheet import SpreadsheetAbstraction
import time

class DataImportUploadBackend(S3UploadBackend):
    def update_filename(self, request, filename):
        return "import/%s/%s.%s" % (request.account.pk, int(time.time()), filename, )

    def upload_complete(self, request, filename, **kwargs):
        self._pool.close()
        self._pool.join()
        self._mp.complete_upload()


        # filename is a file at s3.  Get it.
        f = default_storage.open(filename, 'r')

        # parse the file.
        s = SpreadsheetAbstraction(request.account, f, self.import_type, filename=filename)
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