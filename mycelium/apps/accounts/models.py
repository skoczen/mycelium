from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from managers import AccountDataModelManager, ExplicitAccountDataModelManager, AccountManager
from qi_toolkit.models import TimestampModelMixin, SimpleSearchableModel
from qi_toolkit.helpers import classproperty
from accounts import *

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from johnny import cache as jcache
from zebra.models import StripeCustomer, StripePlan
from zebra.mixins import StripeSubscriptionMixin
import hashlib
import datetime
from dateutil.relativedelta import *
from django.db.models import Sum

class Plan(TimestampModelMixin, StripePlan):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)

    @classmethod
    def monthly_plan(cls):
        return cls.objects.get_or_create(name="Monthly")[0]

    @classmethod
    def yearly_plan(cls):
        return cls.objects.get_or_create(name="Yearly")[0]

class Account(TimestampModelMixin, StripeCustomer, StripeSubscriptionMixin, SimpleSearchableModel):
    name = models.CharField(max_length=255, verbose_name="Organization Name")
    subdomain = models.CharField(max_length=255, unique=True, db_index=True, verbose_name="GoodCloud address (myorganization.agodocloud.com)")
    
    agreed_to_terms = models.BooleanField()
    plan = models.ForeignKey(Plan, blank=True)
    
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
    free_trial_ends_date                = models.DateTimeField(blank=True, null=True) # copied to stripe
    next_billing_date                   = models.DateTimeField(blank=True, null=True) # cached from stripe
    last_four                           = models.CharField(max_length=4, blank=True, null=True) # cached from stripe
    last_stripe_update                  = models.DateTimeField(blank=True, null=True)
    # stripe_customer_id                  = models.CharField(max_length=255, blank=True, null=True)  # provided by zebra.


    is_demo                             = models.BooleanField(default=False)
    was_a_feedback_partner              = models.BooleanField(default=False)

    feature_access_level                = models.IntegerField(default=FEATURE_ACCESS_STATII[0][0], choices=FEATURE_ACCESS_STATII)



    def save(self, *args, **kwargs):
        if not self.id:
            self.signup_date = datetime.datetime.now()
            # self.create_stripe_subscription()
        super(Account,self).save(*args, **kwargs)
            
   
    objects = AccountManager()

    def __unicode__(self):
        return "%s" % self.name

    class Meta(object):
        ordering = ("name",)

    search_fields = ["name", "subdomain"]

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
        # cancel subscription
        if instance.stripe_customer_id:
            c = instance.stripe_customer
            if c and hasattr(c,"subscription"):
                c.cancel_subscription()

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

                    if not self.has_completed_all_challenges and self.free_trial_ends_date and self.free_trial_ends_date.date() >= datetime.date.today():

                        self.free_trial_ends_date = self.signup_date + datetime.timedelta(days=44)
                        
                        # TODO: When stripe updates their API, move to this.
                        # sub = self.stripe_subscription
                        # sub.trial_end = self.free_trial_ends_date
                        # sub.save()

                        c = self.stripe_customer
                        c.update_subscription(plan=MONTHLY_PLAN_NAME, trial_end=self.free_trial_ends_date)

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

    @property
    def feedback_coupon_code(self):
        if self.was_a_feedback_partner:
            return "FEEDBACKTEAM"
        return None

    def create_stripe_subscription(self):
        c = self.stripe_customer
        
        if not self.free_trial_ends_date:
            if datetime.datetime.now() > self.signup_date + datetime.timedelta(days=30):
                # They signed up pre-stripe
                self.free_trial_ends_date = datetime.datetime.now() + datetime.timedelta(minutes=2)
            else:
                self.free_trial_ends_date = self.signup_date + datetime.timedelta(days=30)

        # Create a stripe customer
        c.description=self.name
        c.email=self.primary_useraccount.email
        c.coupon=self.feedback_coupon_code
        c.save()

        if self.is_demo:
            plan_name = FREE_PLAN_NAME
        else:
            plan_name = MONTHLY_PLAN_NAME

        c.update_subscription(plan=plan_name,trial_end=self.free_trial_ends_date)

        self.last_stripe_update = datetime.datetime.now()
        self.save()


    def stripe_subscription_url(self):
        return "https://manage.stripe.com/customers/%s" % self.stripe_customer_id

    def update_account_status(self):
        sub = self.stripe_subscription

        # Possible statuses: canceled, past_due, unpaid, active, trialing
        if sub.status == "trialing":
            self.status = STATUS_FREE_TRIAL
            if not self.free_trial_ends_date and hasattr(sub,"trial_end"):
                self.free_trial_ends_date = datetime.datetime.fromtimestamp(sub.trial_end)
        elif sub.status == "active":
            self.status = STATUS_ACTIVE
        elif sub.status == "past_due":
            self.status = STATUS_ACTIVE_BILLING_ISSUE
        elif sub.status == "unpaid":
            self.status = STATUS_DEACTIVATED
        elif sub.status == "cancelled":
            # should never happen
            self.status = STATUS_DEACTIVATED
        else:
            raise Exception, "Unknown subscription status"
        
        if hasattr(sub,"current_period_end"):
            # For when Stripe upgrades their API
            if type(sub.current_period_end) == type(1):
                self.next_billing_date = datetime.datetime.fromtimestamp(sub.current_period_end)
            else:
                self.next_billing_date = sub.current_period_end
        
        self.last_stripe_update = datetime.datetime.now()
        self.save()
        jcache.invalidate(Account)
        return self
    
    @property
    def has_card_on_file(self):
        return self.last_four != None
    
    @property
    def age_in_months(self):
        return (datetime.datetime.today() - self.signup_date).days / 30


    @property
    def in_free_trial(self):
        # return datetime.datetime.now() <= self.free_trial_ends_date
        return self.status in FREE_TRIAL_STATII

    @property
    def is_active(self):
        return self.status in ACTIVE_SUBSCRIPTION_STATII

    @property
    def is_expired(self):
        return self.status == STATUS_EXPIRED

    @property
    def has_billing_issue(self):
        return self.status in BILLING_PROBLEM_STATII

    @property
    def is_deactivated(self):
        return self.status == STATUS_DEACTIVATED

    @property
    def is_cancelled(self):
        return self.status == STATUS_CANCELLED

    @property
    def has_subscription(self):
        return self.status in HAS_A_SUBSCRIPTION_STATII

    @property
    def cancelled_subscription(self):
        return self.status in CANCELLED_SUBSCRIPTION_STATII

  

    # Aggregates
    @property
    def total_donation_sum(self):
        return self.donation_set.all().aggregate(Sum('amount'))["amount__sum"] or 0

    @property
    def total_volunteer_hours(self):
        return self.completedshift_set.all().aggregate(Sum('duration'))["duration__sum"] or 0

    @classproperty
    @classmethod
    def all_non_demo_accounts(cls):
        return cls.objects.filter(is_demo=False)

    @classproperty
    @classmethod
    def num_non_demo_accounts(cls):
        return cls.all_non_demo_accounts.count()
    
    @classproperty
    @classmethod
    def num_non_demo_accounts_denominator(cls):
        if cls.num_non_demo_accounts > 0:
            return cls.num_non_demo_accounts
        else:
            return 1
    
    @classproperty
    @classmethod
    def all_non_demo_accounts_num_total_people(cls):
        from people.models import Person
        return Person.objects.non_demo.count()

    @classproperty
    @classmethod
    def num_non_demo_accounts_num_total_people_denominator(cls):
        if cls.all_non_demo_accounts_num_total_people> 0:
            return cls.all_non_demo_accounts_num_total_people
        else:
            return 1

    @classproperty
    @classmethod
    def all_non_demo_accounts_num_total_organizations(cls):
        from organizations.models import Organization
        return Organization.objects.non_demo.count()

    @classproperty
    @classmethod
    def all_non_demo_accounts_total_volunteer_hours(cls):
        from volunteers.models import CompletedShift
        return CompletedShift.objects.non_demo.aggregate(Sum('duration'))["duration__sum"] or 0

    @classproperty
    @classmethod
    def all_non_demo_accounts_total_donation_amount(cls):
        from donors.models import Donation
        return Donation.objects.non_demo.aggregate(Sum('amount'))["amount__sum"] or 0

    @classproperty
    @classmethod
    def all_non_demo_accounts_num_total_donations(cls):
        from donors.models import Donation
        return Donation.objects.non_demo.count()

    @classproperty
    @classmethod
    def all_non_demo_accounts_num_tags(cls):
        from generic_tags.models import Tag
        return Tag.objects.non_demo.count()

    @classproperty
    @classmethod
    def all_non_demo_accounts_num_tagged_items(cls):
        from generic_tags.models import TaggedItem
        return TaggedItem.objects.non_demo.count()

    @classproperty
    @classmethod
    def num_non_demo_accounts_num_total_donations_denominator(cls):
        if cls.all_non_demo_accounts_num_total_donations> 0:
            return cls.all_non_demo_accounts_num_total_donations
        else:
            return 1

    @classproperty
    @classmethod
    def all_non_demo_accounts_num_total_groups(cls):
        from groups.models import Group
        return Group.objects.non_demo.count()


    @classproperty
    @classmethod
    def all_non_demo_accounts_num_total_spreadsheets(cls):
        from spreadsheets.models import Spreadsheet
        return Spreadsheet.objects.non_demo.count()


    @classproperty
    @classmethod
    def all_non_demo_accounts_total_number_of_conversations(cls):
        from conversations.models import Conversation
        return Conversation.objects.non_demo.count()


    @classproperty
    @classmethod
    def all_non_demo_accounts_average_num_users(cls):
        return float(UserAccount.objects.filter(account__is_demo=False).count()) / cls.num_non_demo_accounts_denominator

    @classproperty
    @classmethod
    def all_non_demo_accounts_average_num_people(cls):
        return float(cls.all_non_demo_accounts_num_total_people) / cls.num_non_demo_accounts_denominator

    @classproperty
    @classmethod
    def all_non_demo_accounts_average_num_organizations(cls):
        return float(cls.all_non_demo_accounts_num_total_organizations) / cls.num_non_demo_accounts_denominator

    @classproperty
    @classmethod
    def all_non_demo_accounts_average_donation_amount(cls):
        return float(cls.all_non_demo_accounts_total_donation_amount) / cls.num_non_demo_accounts_num_total_donations_denominator


    @classproperty
    @classmethod
    def all_non_demo_accounts_average_number_of_donations_per_account(cls):
        return float(cls.all_non_demo_accounts_num_total_donations) / cls.num_non_demo_accounts_denominator

    @classproperty
    @classmethod
    def all_non_demo_accounts_average_volunteer_hours_per_account(cls):
        return float(cls.all_non_demo_accounts_total_volunteer_hours) / cls.num_non_demo_accounts_denominator

    @classproperty
    @classmethod
    def all_non_demo_accounts_average_volunteer_hours_per_person(cls):
        return float(cls.all_non_demo_accounts_total_volunteer_hours) / cls.num_non_demo_accounts_num_total_people_denominator

    @classproperty
    @classmethod
    def all_non_demo_accounts_average_tags_per_person(cls):
        return float(cls.all_non_demo_accounts_num_tags) / cls.num_non_demo_accounts_num_total_people_denominator
    
    @classproperty
    @classmethod
    def all_non_demo_accounts_average_tags_per_account(cls):
        return float(cls.all_non_demo_accounts_num_tags) / cls.num_non_demo_accounts_denominator

    @classproperty
    @classmethod
    def all_non_demo_accounts_average_taggeditems_per_person(cls):
        return float(cls.all_non_demo_accounts_num_tagged_items) / cls.num_non_demo_accounts_num_total_people_denominator
    
    @classproperty
    @classmethod
    def all_non_demo_accounts_average_taggeditems_per_account(cls):
        return float(cls.all_non_demo_accounts_num_tagged_items) / cls.num_non_demo_accounts_denominator

    @classproperty
    @classmethod
    def all_non_demo_accounts_average_groups_per_account(cls):
        return float(cls.all_non_demo_accounts_num_total_groups) / cls.num_non_demo_accounts_denominator

    @classproperty
    @classmethod
    def all_non_demo_accounts_average_spreadsheets_per_account(cls):
        return float(cls.all_non_demo_accounts_num_total_spreadsheets) / cls.num_non_demo_accounts_denominator

    @classproperty
    @classmethod
    def all_non_demo_accounts_average_number_of_conversations(cls):
        return float(cls.all_non_demo_accounts_total_number_of_conversations) / cls.num_non_demo_accounts_denominator    



    @property
    def num_people(self):
        return self.person_set.count()

    @property
    def num_people_denominator(self):
        if self.num_people > 0:
            return self.num_people
        else:
            return 1

    @property
    def num_organizations(self):
        return self.organization_set.count()


    @property
    def num_conversations(self):
        return self.conversation_set.count()


    @property
    def num_donations(self):
        return self.donation_set.count()

    @property
    def num_donations_denominator(self):
        if self.num_donations > 0:
            return self.num_donations
        else:
            return 1

    @property
    def total_donations(self):
        return self.donation_set.all().aggregate(Sum('amount'))["amount__sum"] or 0

    @property
    def avg_donation(self):
        return float(self.total_donations) / self.num_donations_denominator

    @property
    def num_volunteer_hours(self):
        return self.completedshift_set.all().aggregate(Sum('duration'))["duration__sum"] or 0

    @property
    def avg_vol_hours_per_person(self):
        return float(self.num_volunteer_hours) / self.num_people_denominator

    @property
    def num_tags(self):
        return self.tag_set.count()

    @property
    def num_taggeditems(self):
        return self.taggeditem_set.count()

    @property
    def avg_tags_per_person(self):
        return float(self.num_taggeditems) / self.num_people_denominator

    @property
    def num_groups(self):
        return self.group_set.count()
    
    @property
    def num_spreadsheets(self):
        return self.spreadsheet_set.count()

    @property
    def has_beta_access(self):
        return self.feature_access_level >= FEATURE_ACCESS_STATII[1][0]

    @property
    def has_alpha_access(self):
        return self.feature_access_level >= FEATURE_ACCESS_STATII[2][0]
    
    @property
    def has_bleeding_edge_access(self):
        return self.feature_access_level >= FEATURE_ACCESS_STATII[3][0]
    
    @property
    def has_access_to_level(self, access_level):
        return self.feature_access_level >= access_level

    def recent_activities(self):
        return self.action_set.all()


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
            if " " in self.full_name:
                return self.full_name[:self.full_name.find(" ")]
            else:
                return self.full_name

    @property
    def uservoice_sso_token(self):
        from Crypto.Cipher import AES
        import base64
        import urllib
        import operator
        import array
        import simplejson as json

        message = {
          "guid" : self.user.id,
          "display_name" : self.full_name,
          "email" : self.email,
        }
        block_size = 16
        mode = AES.MODE_CBC

        # If you're acme.uservoice.com then this value would be 'acme'
        uservoice_subdomain = 'goodcloud'

        # Get this from your UserVoice General Settings page
        sso_key = "87071942d51dbe690b0d5d1b9b832715"

        iv = "OpenSSLforPython"

        json = json.dumps(message, separators=(',',':'))

        salted = sso_key+uservoice_subdomain
        saltedHash = hashlib.sha1(salted).digest()[:16]

        json_bytes = array.array('b', json[0 : len(json)]) 
        iv_bytes = array.array('b', iv[0 : len(iv)])

        # # xor the iv into the first 16 bytes.
        for i in range(0, 16):
            json_bytes[i] = operator.xor(json_bytes[i], iv_bytes[i])

        pad = block_size - len(json_bytes.tostring()) % block_size
        data = json_bytes.tostring() + pad * chr(pad)
        aes = AES.new(saltedHash, mode, iv)
        encrypted_bytes = aes.encrypt(data)

        param_for_uservoice_sso = urllib.quote(base64.b64encode(encrypted_bytes))
        return param_for_uservoice_sso

    def recent_activities(self):
        return self.action_set.all()


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


def recurring_payment_failed(sender, **kwargs):
    account = kwargs["customer"]
    full_json = kwargs["full_json"]
    account.update_account_status()
    send_mail("Recurring payment failed: %s" % (account,), "%s" % render_to_string("accounts/recurring_payment_failed.txt", locals()), settings.SERVER_EMAIL, [e[1] for e in settings.MANAGERS] )    

def invoice_ready(sender, **kwargs):
    account = kwargs["customer"]
    full_json = kwargs["full_json"]
    pass

def recurring_payment_succeeded(sender, **kwargs):
    account = kwargs["customer"]
    full_json = kwargs["full_json"]
    account.update_account_status()

def subscription_trial_ending(sender, **kwargs):
    account = kwargs["customer"]
    full_json = kwargs["full_json"]
    # Email Steven & Tom
    send_mail("Account trial about to expire: %s" % (account,), "%s" % render_to_string("accounts/free_trial_nearly_done.txt", locals()), settings.SERVER_EMAIL, [e[1] for e in settings.MANAGERS] )    

def subscription_final_payment_attempt_failed(sender, **kwargs):
    account = kwargs["customer"]
    full_json = kwargs["full_json"]
    send_mail("Account deactivated for nonpayment: %s" % (account,), "%s" % render_to_string("accounts/deactivated_for_nonpayment.txt", locals()), settings.SERVER_EMAIL, [e[1] for e in settings.MANAGERS] )    
    account.update_account_status()


from zebra.signals import *
zebra_webhook_recurring_payment_failed.connect(recurring_payment_failed)
zebra_webhook_invoice_ready.connect(invoice_ready)
zebra_webhook_recurring_payment_succeeded.connect(recurring_payment_succeeded)
zebra_webhook_subscription_trial_ending.connect(subscription_trial_ending)
zebra_webhook_subscription_final_payment_attempt_failed.connect(subscription_final_payment_attempt_failed)

from django.db.models.signals import post_save, pre_delete
from rules.tasks import populate_rule_components_for_an_account_signal_receiver
post_save.connect(populate_rule_components_for_an_account_signal_receiver,sender=Account)
post_save.connect(Account.create_default_tagsets,sender=Account)
pre_delete.connect(Account.pre_delete_cleanup,sender=Account)


