from django.db import models
from django.utils.translation import ugettext as _
from qi_toolkit.models import SimpleSearchableModel, TimestampModelMixin

from accounts.models import AccountBasedModel

# class DataImport(SimpleSearchableModel, TimestampModelMixin):
#     search_fields = ["",]
#     pass