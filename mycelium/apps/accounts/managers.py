from django.db import models

class AccountDataModelManager(models.Manager):


    def __call__(self, *args, **kwargs):
        # if not "request" in kwargs or "account" in kwargs:
        #     raise Exception, "Missing Request and/or Account!"
        # else:
        # account = None
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
            # print self.account
            return super(AccountDataModelManager, self).get_query_set().filter(account=self.account)
        else:
            # This is horribly, horribly bad, and I know it.  If there's a better way, we should find it.
            import inspect
            # frm = inspect.stack()[1]
            # mod = inspect.getmodule(frm[0])
            # if mod.__name__[:len("django.")] == "django.":
            print inspect.getmodule(inspect.stack()[1][0]).__name__
            
            if inspect.getmodule(inspect.stack()[1][0]).__name__[:7] == "django.":
                return super(AccountDataModelManager, self).get_query_set()
            else:
                raise Exception, "Missing Request and/or Account!"

