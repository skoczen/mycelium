from accounts.forms import AccountBasedModelForm
from spreadsheets.models import Spreadsheet

class SpreadsheetForm(AccountBasedModelForm):
    class Meta:
        model = Spreadsheet
        fields = ("account", "name", "group", "spreadsheet_template")

    