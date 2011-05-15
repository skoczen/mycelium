from django.template import RequestContext
from django.conf import settings
from accounts.managers import get_or_404_by_account
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from qi_toolkit.helpers import *
from django.middleware.csrf import get_token
from ajaxuploader.views import AjaxFileUploader

@render_to("import/list.html")
def list(request):
    # TODO: this is obnoxious.  Fix it.
    section = "more"
    return locals()

@render_to("import/start.html")
def start(request):
    # TODO: this is obnoxious.  Fix it.
    section = "more"
    csrf_token = get_token( request )

    return locals()

@render_to("import/review.html")
def review(request, import_id):
    # TODO: this is obnoxious.  Fix it.
    section = "more"
    return locals()

class DataImportAjaxFileUploader(AjaxFileUploader):
    def _update_filename(self, request, filename):
        import time
        return "import/%s/%s.%s" % (request.account.pk, int(time.time()), filename, )

    def _upload_complete(self, request, filename):
        print "Need to save %s to the database!"  % filename

data_import_uploader = DataImportAjaxFileUploader()