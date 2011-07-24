from django.db import models
from django.shortcuts import get_object_or_404
import datetime
from accounts import ACTIVE_SUBSCRIPTION_STATII, BILLING_PROBLEM_STATII

def get_or_404_by_account(cls, account, id, using=None):
    if hasattr(account,"account"):
        account = account.account

    return get_object_or_404(cls.objects_by_account(account),pk=id)
    
    # if not using:
        # return get_object_or_404(cls.objects_by_account(account),pk=id)
    # else:
    #     return get_object_or_404(cls.objects_by_account(account).using(using),pk=id)

class AccountManager(models.Manager):

    def week_range(self, d1, d2):
        return self.filter(signup_date__range=(d1, d2)).filter(is_demo=False).order_by("-signup_date")

    @property
    def week_1(self):
        target = datetime.datetime.now() - datetime.timedelta(days=7)
        return self.filter(signup_date__gte=target).filter(is_demo=False)
    
    @property
    def week_2(self):
        d1 = datetime.datetime.today() - datetime.timedelta(days=14)
        d2 = datetime.datetime.today() - datetime.timedelta(days=7)
        return self.week_range(d1,d2)
    
    @property
    def week_3(self):
        d1 = datetime.datetime.today() - datetime.timedelta(days=21)
        d2 = datetime.datetime.today() - datetime.timedelta(days=14)
        return self.week_range(d1,d2)
    
    @property
    def week_4(self):
        d1 = datetime.datetime.today() - datetime.timedelta(days=30)
        d2 = datetime.datetime.today() - datetime.timedelta(days=21)
        return self.week_range(d1,d2)
    
    @property
    def active(self):
        return self.filter(status__in=ACTIVE_SUBSCRIPTION_STATII)

    @property
    def non_demo(self):
        return self.filter(is_demo=False)

    @property
    def billing_problem(self):
        return self.filter(status__in=BILLING_PROBLEM_STATII)

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
    @property
    def non_demo(self):
        return self.filter(account__is_demo=False).all()


class ExplicitAccountDataModelManager(models.Manager):
    def __call__(self, account, *args, **kwargs):
        if hasattr(account, "account"):
            self.account = account.account
        else:
            self.account = account

        return self.get_query_set()

    def get_query_set(self):
        return super(ExplicitAccountDataModelManager, self).get_query_set().filter(account=self.account)
