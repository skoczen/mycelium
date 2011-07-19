from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from managers import AccountDataModelManager, ExplicitAccountDataModelManager, AccountManager
from qi_toolkit.models import TimestampModelMixin
from accounts import ACCOUNT_STATII, CHARGIFY_STATUS_MAPPING, HAS_A_SUBSCRIPTION_STATII, CANCELLED_SUBSCRIPTION_STATII, ACTIVE_SUBSCRIPTION_STATII
from django.conf import settings
from pychargify.api import ChargifySubscription, ChargifyCustomer, Chargify
import hashlib
import datetime
from dateutil.relativedelta import *

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

    was_a_feedback_partner               = models.BooleanField(default=False)
    challenge_has_imported_contacts      = models.BooleanField(default=False)
    challenge_has_set_up_tags            = models.BooleanField(default=False)
    challenge_has_added_board            = models.BooleanField(default=False)
    challenge_has_created_other_accounts = models.BooleanField(default=False)
    challenge_has_downloaded_spreadsheet = models.BooleanField(default=False)
    challenge_has_submitted_support      = models.BooleanField(default=False)
    challenge_has_added_a_donation       = models.BooleanField(default=False)
    challenge_has_logged_volunteer_hours = models.BooleanField(default=False)
    has_completed_all_challenges         = models.BooleanField(default=False)  # A separate field to support when the challenges change.
    has_completed_any_challenges         = models.BooleanField(default=False)  

    status                              = models.IntegerField(default=ACCOUNT_STATII[0][0], choices=ACCOUNT_STATII)
    signup_date                         = models.DateTimeField(null=True, default=datetime.datetime.now())
    last_billing_date                   = models.DateTimeField(blank=True, null=True)                # chargify sub: current_period_started_at
    chargify_subscription_id            = models.IntegerField(blank=True, null=True)
    chargify_state                      = models.CharField(max_length=255, blank=True, null=True)
    chargify_cancel_at_end_of_period    = models.BooleanField(default=False)
    chargify_next_assessment_at         = models.DateTimeField(blank=True, null=True)
    chargify_last_four                  = models.CharField(blank=True, null=True, max_length=4)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.signup_date = datetime.datetime.now()
        super(Account,self).save(*args, **kwargs)
            

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)

    @property
    def primary_useraccount(self):
        return self.useraccount_set.order_by("created_at").all()[0]

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
        # delete group rules
        for gr in instance.grouprule_set.all():
            gr.delete()
        # delete employees
        for e in instance.employee_set.all():
            e.delete()


    def check_challenge_progress(self):
        """This function checks each uncompleted challenge to see if it's been done,
           and updates the boolean fields as needed"""

        if not self.has_completed_all_challenges:
            from generic_tags.models import Tag
            from groups.models import Group
            from donors.models import Donation
            from volunteers.models import CompletedShift
            from data_import.models import DataImport
            from spreadsheets.models import Spreadsheet

            if not self.challenge_has_imported_contacts:
                if DataImport.objects_by_account(self).count() > 0:
                    self.challenge_has_imported_contacts = True

            if not self.challenge_has_set_up_tags:
                # One non-standard tag.
                if Tag.objects_by_account(self).count() > 0:
                    self.challenge_has_set_up_tags = True
                                
            if not self.challenge_has_added_board:
                # created a tag that contains "board"
                if Tag.objects_by_account(self).filter(name__icontains="board").count() > 0:
                    
                    # and, created a board group with at least one rule on tag
                    if Group.objects_by_account(self).filter(name__icontains="board").count() > 0:
                        for g in Group.objects_by_account(self).all():
                            for r in g.rules.all():
                                if r.is_valid and "board" in r.cleaned_right_side_value.lower():
                                    self.challenge_has_added_board = True


            if not self.challenge_has_created_other_accounts:
                if self.useraccount_set.all().count() > 1:
                    self.challenge_has_created_other_accounts = True

            if not self.challenge_has_downloaded_spreadsheet:
                if Spreadsheet.objects_by_account(self).count() > 0:
                    self.challenge_has_downloaded_spreadsheet = True

            if not self.challenge_has_submitted_support:
                pass
            
            if not self.challenge_has_added_a_donation:
                if Donation.objects_by_account(self).count() > 0:
                    self.challenge_has_added_a_donation = True
                
            if not self.challenge_has_logged_volunteer_hours:
                if CompletedShift.objects_by_account(self).count() > 0:
                    self.challenge_has_logged_volunteer_hours = True

            if not self.has_completed_all_challenges:
                # self.challenge_has_submitted_support and \
                if self.challenge_has_imported_contacts and self.challenge_has_set_up_tags and\
                    self.challenge_has_added_board and self.challenge_has_created_other_accounts and\
                    self.challenge_has_downloaded_spreadsheet and \
                    self.challenge_has_added_a_donation and self.challenge_has_logged_volunteer_hours:

                    self.has_completed_all_challenges = True

            if not self.has_completed_any_challenges:
                #  self.challenge_has_submitted_support or\
                if self.challenge_has_imported_contacts or self.challenge_has_set_up_tags or\
                    self.challenge_has_added_board or self.challenge_has_created_other_accounts or\
                    self.challenge_has_downloaded_spreadsheet or\
                    self.challenge_has_added_a_donation or self.challenge_has_logged_volunteer_hours:

                    self.has_completed_any_challenges = True

            self.save()
    
    def upcoming_birthdays(self):
        from people.models import Person, NORMALIZED_BIRTH_YEAR
        from dashboard import NUMBER_BIRTHDAYS_OF_TO_SHOW
        import datetime
        from django.db.models import Q

        today = datetime.date.today()
        normalized_today = datetime.date(day=today.day, month=today.month, year=NORMALIZED_BIRTH_YEAR)
        normalized_end_date = normalized_today + datetime.timedelta(days=30)
        if today.month == 12 and today.day > 24:
            normalized_end_date = normalized_end_date - datetime.timedelta(years=1)
            if Person.objects_by_account(self).filter(normalized_birthday__gte=today).count() + \
               Person.objects_by_account(self).filter(normalized_birthday__lt=normalized_end_date).count() > NUMBER_BIRTHDAYS_OF_TO_SHOW-1:

                birthday_people = Person.objects_by_account(self).filter(Q(normalized_birthday__lt=normalized_end_date) | Q(normalized_birthday__gte=today)).all()
            else:
                birthday_people = Person.objects_by_account(self).filter(Q(normalized_birthday__lt=normalized_end_date) | Q(normalized_birthday__gte=today))
        else:
            if Person.objects_by_account(self).filter(normalized_birthday__lt=normalized_end_date, normalized_birthday__gte=today).count() > NUMBER_BIRTHDAYS_OF_TO_SHOW-1:
                birthday_people = Person.objects_by_account(self).filter(normalized_birthday__lt=normalized_end_date, normalized_birthday__gte=today)
            else:
                birthday_people = Person.objects_by_account(self).filter(normalized_birthday__gte=normalized_today) 
        
        if birthday_people:
            return birthday_people.all().order_by("birth_month","birth_day", "first_name", "last_name")[:NUMBER_BIRTHDAYS_OF_TO_SHOW]
        return None

    def create_subscription(self):
        chargify = Chargify(settings.CHARGIFY_API, settings.CHARGIFY_SUBDOMAIN)
        customer = chargify.Customer()
        customer.first_name = self.primary_useraccount.full_name[:self.primary_useraccount.full_name.find(" ")]
        customer.last_name = self.primary_useraccount.full_name[self.primary_useraccount.full_name.find(" ")+1:]
        customer.organization = self.name
        customer.reference = "%s" % self.id
        customer.email = self.primary_useraccount.user.email
        customer.save()

        customer = chargify.Customer()
        customer = customer.getByReference(self.pk)

        subscription = chargify.Subscription()
        subscription.product_handle = settings.CHARGIFY_PRODUCT_HANDLE
        subscription.customer_reference = "%s" % self.id
        # subscription.next_billing_at = self.free_trial_ends.isoformat()
        subscription.save()

        subscription = chargify.Subscription()
        subscription = subscription.getByCustomerId(customer.id)[0]

        self.chargify_subscription_id = subscription.id
        self.save()

    @property
    def chargify_subscription(self):
        chargify = Chargify(settings.CHARGIFY_API, settings.CHARGIFY_SUBDOMAIN)
        subscription = chargify.Subscription()
        return subscription.getBySubscriptionId(self.chargify_subscription_id)


    def update_account_status(self):
        chargify_sub = self.chargify_subscription
        self.last_billing_date = chargify_sub.current_period_started_at
        self.chargify_state = chargify_sub.state
        
        self.chargify_cancel_at_end_of_period = chargify_sub.cancel_at_end_of_period == "true"

        self.chargify_next_assessment_at = chargify_sub.current_period_ends_at
        if chargify_sub.credit_card:
            self.chargify_last_four = chargify_sub.credit_card.masked_card_number[chargify_sub.credit_card.masked_card_number.rfind("-")+1:]
        else:
            self.chargify_last_four = None

        self.status = CHARGIFY_STATUS_MAPPING[chargify_sub.state][0]
        self.save()

        return self
    

    @property
    def free_trial_ends(self):
        return self.signup_date + relativedelta(months=+1)

    @property
    def in_free_trial(self):
        return datetime.datetime.now() <= self.free_trial_ends

    @property
    def is_active(self):
        return self.status in ACTIVE_SUBSCRIPTION_STATII

    @property
    def is_expired(self):
        return self.status == ACCOUNT_STATII[1][0]

    @property
    def has_billing_issue(self):
        return self.status == ACCOUNT_STATII[3][0]

    @property
    def is_on_hold(self):
        return self.status == ACCOUNT_STATII[4][0]

    @property
    def is_cancelled(self):
        return self.status == ACCOUNT_STATII[5][0]

    @property
    def has_subscription(self):
        return self.status in HAS_A_SUBSCRIPTION_STATII

    @property
    def cancelled_subscription(self):
        return self.status in CANCELLED_SUBSCRIPTION_STATII

    @property
    def has_card_on_file(self):
        return self.chargify_last_four != None

    @property
    def chargify_manage_url(self):
        h = hashlib.new('sha1')
        h.update("update_payment--%s--%s" % (self.chargify_subscription_id, settings.CHARGIFY_SHARED_KEY))

        return "https://%(subdomain)s.chargify.com/update_payment/%(sub_id)s/%(message)s" % {
            'subdomain': settings.CHARGIFY_SUBDOMAIN,
            'sub_id': self.chargify_subscription_id,
            'message': h.hexdigest()[:10]
        }
        
    
    @property
    def chargify_signup_url(self):
        return "%(HOSTED_URL)s?organization=%(org_name)s&reference=%(account_pk)s" % {
                  'HOSTED_URL' : settings.CHARGIFY_HOSTED_SIGNUP_URL,
                  'org_name' : self.name,
                  'account_pk': self.pk,
                  }

    objects = AccountManager()

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

    show_challenges_complete_section     = models.BooleanField(default=True)    

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
        return "%s" % (self.nickname_or_full_name,)

    class Meta(object):
        ordering = ("account", "nickname", "user__first_name", "access_level","user")


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
