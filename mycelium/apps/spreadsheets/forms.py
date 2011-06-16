from accounts.forms import AccountBasedModelForm
from spreadsheets.models import Spreadsheet
from django.forms.widgets import RadioSelect

class SpreadsheetForm(AccountBasedModelForm):
    class Meta:
        model = Spreadsheet
        fields = ("account", "name", "group", "spreadsheet_template", "default_filetype")
        widgets = {
            'default_filetype': RadioSelect,
            'spreadsheet_template': RadioSelect
        }

    def __init__(self, *args, **kwargs):
        super(SpreadsheetForm, self).__init__(*args, **kwargs)
        self.fields["group"].empty_label = "All Contacts"
