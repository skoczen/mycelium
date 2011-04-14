from django.db import models

class AccountDataModelManager(models.Manager):
    def get_query_set(self, request):
        return super(AccountDataModelManager, self).get_query_set().filter(account_id=request.account.pk)