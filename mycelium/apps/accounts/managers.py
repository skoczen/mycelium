from django.db import models
from django.shortcuts import get_object_or_404

def get_or_404_by_account(cls, account, id):
    if hasattr(account,"account"):
        account = account.account
    return get_object_or_404(cls.objects_by_account(account),pk=id)

class AccountDataModelManager(models.Manager):
    def __call__(self, *args, **kwargs):
        if "request" in kwargs:
            self.account = kwargs["request"].account
            del kwargs["request"]    
        
        if "account" in kwargs:
            self.account = kwargs["account"]
            del kwargs["account"]
            
        if not hasattr(self,"account") and len(args) > 0:
            if hasattr(args[0],"account"):
                self.account = args[0].account
            else:
                self.account = args[0]

        return self.get_query_set()

    def get_query_set(self):
        if hasattr(self,"account") and self.account:

            return super(AccountDataModelManager, self).get_query_set().filter(account=self.account)
        else:
            # This is horribly, horribly bad, and I know it.  If there's a better way, we should find it.
            import inspect
            if inspect.getmodule(inspect.stack()[1][0]).__name__[:7] == "django.":
                return super(AccountDataModelManager, self).get_query_set()
            else:
                raise Exception, "Missing Request and/or Account!"


class ExplicitAccountDataModelManager(models.Manager):
    def __call__(self, account, *args, **kwargs):
        if hasattr(account, "account"):
            self.account = account.account
        else:
            self.account = account

        return self.get_query_set()

    def get_query_set(self):
        return super(ExplicitAccountDataModelManager, self).get_query_set().filter(account=self.account)
