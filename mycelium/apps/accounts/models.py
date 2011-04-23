from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from managers import AccountDataModelManager, ExplicitAccountDataModelManager


class Plan(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)

    @classmethod
    def monthly_plan(cls):
        return cls.objects.get_or_create(name="Monthly")[0]

class Account(models.Model):
    name = models.CharField(max_length=255, verbose_name="Organization Name")
    subdomain = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="GoodCloud address (myorganization.agodocloud.com)")
    is_active = models.BooleanField(default=True)
    plan = models.ForeignKey(Plan, blank=True)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)

    def namespaced_username_for_username(self, username):
        return "a%s_%s" % (self.pk, username)

    def create_useraccount(self, full_name=None, username=None, password=None, email=None, access_level=None, user=None):
        assert full_name != None and username != None and password != None and access_level != None
        if not user:
            if User.objects.filter(username=self.namespaced_username_for_username(username)).count() != 0:
                user = User.objects.get(username=self.namespaced_username_for_username(username))
            else:
                user = User.objects.create_user(self.namespaced_username_for_username(username), email, password)

        user.first_name=full_name
        user.save()
        
        return UserAccount.objects.get_or_create(user=user, account=self, access_level=access_level)[0]

    @classmethod
    def create_default_tagsets(cls, instance, created=None, *args, **kwargs):
        from generic_tags.models import TagSet
        if instance and created:
            TagSet.create_default_tagsets_for_an_account(instance)
    
    @classmethod
    def pre_delete_cleanup(cls, instance, created=None, *args, **kwargs):
        # delete user accounts
        for ua in instance.useraccount_set.all():
            ua.user.delete()

class AccessLevel(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name

    @classmethod
    def admin(cls):
        return cls.objects.get(name__iexact="Admin")
    @classmethod
    def staff(cls):
        return cls.objects.get(name__iexact="Staff")

    @classmethod
    def volunteer(cls):
        return cls.objects.get(name__iexact="Volunteer")

    class Meta(object):
        ordering = ("name",)


class UserAccount(models.Model):
    user = models.ForeignKey(User, db_index=True)
    account = models.ForeignKey(Account, db_index=True)
    access_level = models.ForeignKey(AccessLevel)
    # nickname = models.CharField(max_length=255)
    
    @property
    def denamespaced_username(self):
        return self.user.username[(2+len("%s"%self.account.pk)):]

    def __unicode__(self):
        return "%s with %s" % (self.denamespaced_username, self.account)

    class Meta(object):
        ordering = ("account","access_level","user")


class AccountBasedModel(models.Model):
    account = models.ForeignKey(Account, db_index=True)

    objects = AccountDataModelManager()
    raw_objects = models.Manager()
    objects_by_account = ExplicitAccountDataModelManager()


    class Meta(object):
        abstract = True

from django.db.models.signals import post_save, pre_delete
from rules.tasks import populate_rule_components_for_an_account_signal_receiver
post_save.connect(populate_rule_components_for_an_account_signal_receiver,sender=Account)
post_save.connect(Account.create_default_tagsets,sender=Account)
pre_delete.connect(Account.pre_delete_cleanup,sender=Account)
