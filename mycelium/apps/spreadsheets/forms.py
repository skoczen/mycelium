from accounts.forms import AccountBasedModelForm
from spreadsheets.models import Spreadsheet
from django.forms.widgets import RadioSelect

class SpreadsheetForm(AccountBasedModelForm):
    class Meta:
        model = Spreadsheet
        fields = ("account", "name", "group", "spreadsheet_template", "default_filetype")
        widgets = {
            'default_filetype': RadioSelect
        }
    