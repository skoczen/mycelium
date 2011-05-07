from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from managers import AccountDataModelManager, ExplicitAccountDataModelManager
from qi_toolkit.models import TimestampModelMixin

class Plan(TimestampModelMixin):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)

    @classmethod
    def monthly_plan(cls):
        return cls.objects.get_or_create(name="Monthly")[0]

class Account(TimestampModelMixin):
    name = models.CharField(max_length=255, verbose_name="Organization Name")
    subdomain = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="GoodCloud address (myorganization.agodocloud.com)")
    is_active = models.BooleanField(default=True)
    agreed_to_terms = models.BooleanField()
    plan = models.ForeignKey(Plan, blank=True)

    challenge_has_imported_contacts      = models.BooleanField(default=False)
    challenge_has_set_up_tags            = models.BooleanField(default=False)
    challenge_has_added_board            = models.BooleanField(default=False)
    challenge_has_created_other_accounts = models.BooleanField(default=False)
    challenge_has_downloaded_spreadsheet = models.BooleanField(default=False)
    challenge_submitted_support          = models.BooleanField(default=False)
    has_completed_all_challenges         = models.BooleanField(default=False)  # A separate field to support when the challenges change.
    has_completed_any_challenges         = models.BooleanField(default=False)  
    
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


    def check_challenge_progress(self):
        """This function checks each uncompleted challenge to see if it's been done,
           and updates the boolean fields as needed"""
        
        pass

class AccessLevel(TimestampModelMixin):
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


class UserAccount(TimestampModelMixin):
    user = models.ForeignKey(User, db_index=True)
    account = models.ForeignKey(Account, db_index=True)
    access_level = models.ForeignKey(AccessLevel)
    nickname = models.CharField(max_length=255, blank=True, null=True)
    
    @property
    def denamespaced_username(self):
        return self.user.username[(2+len("%s"%self.account.pk)):]

    @property
    def full_name(self):
        return self.user.first_name

    @property
    def username(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

    @property
    def is_admin(self):
        return self.access_level == AccessLevel.admin()

    @property
    def is_staff(self):
        return self.access_level == AccessLevel.staff()

    @property
    def is_volunteer(self):
        return self.access_level == AccessLevel.volunteer()

    @property
    def nickname_or_full_name(self):
        if self.nickname:
            return self.nickname
        else:
            return self.full_name
    
    @property
    def best_nickname_guess(self):
        if self.nickname:
            return self.nickname
        else:
            return self.full_name[:self.full_name.find(" ")]

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
