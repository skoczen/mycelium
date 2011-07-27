from django.utils.translation import ugettext as _
from spreadsheets.export_templates import SPREADSHEET_TEMPLATES
NO_NAME_STRING_SPREADSHEET = _("Unnamed Spreadsheet")

SPREADSHEET_TEMPLATE_CHOICES = [(t.template_type, t) for t in SPREADSHEET_TEMPLATES]
