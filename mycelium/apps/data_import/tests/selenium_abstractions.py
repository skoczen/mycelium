# encoding: utf-8
import time
from test_factory import Factory
from django.conf import settings
import os

class DataImportTestAbstractions(object):
    
    def get_to_import_list(self):
        sel = self.selenium
        self.open("/")
        sel.wait_for_page_to_load(30000)
        sel.click("css=.admin_btn")
        sel.wait_for_page_to_load(30000)
        sel.click("css=.data_import_btn")
        sel.wait_for_page_to_load(30000)
        assert sel.is_text_present("Data Import History")

    def get_to_start_import_page(self):
        self.get_to_import_list()
        sel = self.selenium
        sel.click("css=.start_import_btn")
        sel.wait_for_page_to_load(30000)
        assert sel.is_text_present("Start Data Import")

    def set_upload_file(self, filename):
        sel = self.selenium
        # sel.focus("css=.qq-uploader input[name=file]")
        sel.attach_file("css=.qq-uploader input[name=file]","file://%s" % os.path.join(settings.PROJECT_ROOT,"apps","data_import","tests","test_spreadsheets",filename))
        # sel.focus("css=.import_type_people input")
        # sel.click("css=.qq-uploader")

        # sel.get_eval("this.browserbot.getUserWindow().document.uploader._handler.add("foo.xls");");


        # GetEval("this.browserbot.getUserWindow().functionUnderTest().isNaN();"
        # $sel->type('browseid', '/home/dir/filename');
        # $sel->focus('uploadid');
        # $sel->click('click');