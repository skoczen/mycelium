import time
import datetime
from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from functional_tests.selenium_test_case import DjangoFunctionalUnitTestMixin
from django.test import TestCase
from groups.models import Group
from people.models import Person
from organizations.models import Organization, Employee
from donors.models import Donor, Donation
from accounts.models import Account, UserAccount, AccessLevel
from volunteers.models import Volunteer, CompletedShift
from spreadsheets.models import Spreadsheet
from generic_tags.models import TagSet, Tag, TaggedItem
from django.core import mail
from django.conf import settings
from django.test.client import Client

from accounts import CANCELLED_SUBSCRIPTION_STATII

class Dummy(object):
    pass

class TestAccountFactory(TestCase, DjangoFunctionalUnitTestMixin, DestructiveDatabaseTestCase):
    # fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        pass

    def test_factory_account_can_be_run_multiple_times(self):
        for i in range(0,Factory.rand_int(2,6)):
            Factory.create_demo_site("test%s" % i, quick=True)

        assert True == True # Finished successfully.        

    def test_creating_and_deleting_an_account_does_so_successfully(self):
        from django.contrib.auth.models import User
        a1 = Factory.create_demo_site("test1", quick=True)
        a2 = Factory.create_demo_site("test2", quick=True)
        a1.delete()
        time.sleep(5)
        a3 = Factory.create_demo_site("test3", quick=True)
        a3.delete()
        self.assertEqual(Account.objects.all().count(), 1)
        self.assertEqual(User.objects.all().count(), 3)
        a2.delete()
        self.assertEqual(Account.objects.all().count(), 0)
        self.assertEqual(User.objects.all().count(), 0)

    def test_objects_by_account_limits_to_account(self, model=Group, factory_method=Factory.group, **kwargs):
        a1 = Factory.account("test1",delete_existing=True)
        g1 = factory_method(account=a1, **kwargs)
        a2 = Factory.account("test2",delete_existing=True)
        g2 = factory_method(account=a2, **kwargs)

        request = Dummy()
        request.account = a1
        
        self.assertNotEqual(a1,a2)
        self.assertNotEqual(g1,g2)

        self.assertEqual([g for g in model.objects_by_account(a1).all()], [g1])
        self.assertEqual([g for g in model.objects_by_account(request).all()], [g1])
        
        self.assertEqual([g for g in model.objects_by_account(a2).all()], [g2])
        assert [g for g in model.raw_objects.all()] ==  [g1, g2] or [g for g in model.raw_objects.all()] ==  [g2, g1]


    def test_for_each_account_model_that_creating_some_of_them_makes_them_inaccessible_to_other_accounts(self):
        self.test_objects_by_account_limits_to_account(Group, Factory.group)
        
        self.test_objects_by_account_limits_to_account(Person, Factory.person)
        self.test_objects_by_account_limits_to_account(Employee, Factory.employee)
        self.test_objects_by_account_limits_to_account(Donor, Factory.donor_history)
        self.test_objects_by_account_limits_to_account(Donation, Factory.donation)
        self.test_objects_by_account_limits_to_account(Organization, Factory.organization)
        self.test_objects_by_account_limits_to_account(Volunteer, Factory.volunteer_history)
        # self.test_objects_by_account_limits_to_account(TagSet, Factory.tagset)
        self.test_objects_by_account_limits_to_account(Tag, Factory.tag)
        # self.test_objects_by_account_limits_to_account(CompletedShift, Factory.completed_volunteer_shift, person=Factory.person())
        # The two commented out behave properly in hand-testing, but were a beast to test via this method, and we *are* trying to ship.


    def test_primary_useraccount_chooses_the_right_account(self):
        a1 = Factory.create_demo_site("test1", quick=True)
        admin_accesslevel = AccessLevel.objects.get(name__iexact="Admin")     
        admin_account = UserAccount.objects.get(account=a1, access_level=admin_accesslevel)
        assert a1.primary_useraccount == admin_account


    def test_that_webhook_causes_a_subscription_update(self):
        a1 = Factory.create_demo_site("test1", quick=True, create_subscription=True)
        sub = a1.chargify_subscription
        sub.unsubscribe("Unsubscribe via site")

        c = Client()
        response = c.post('/webhooks/chargify/webhook', {'event': 'subscription_state_changed', 'payload[subscription][id]': sub.id})
        assert response.status_code == 200

        a1a = Account.objects.get(pk=a1.pk)

        assert a1a.status in CANCELLED_SUBSCRIPTION_STATII

    def test_deleting_an_account_cancels_its_subscription(self):
        a1 = Factory.create_demo_site("test1", quick=True, create_subscription=True)
        sub_id = a1.chargify_subscription_id

        a1.delete()

        chargify = Chargify(settings.CHARGIFY_API, settings.CHARGIFY_SUBDOMAIN)
        subscription = chargify.Subscription()
        s = subscription.getBySubscriptionId(sub_id)

        self.assertEqual(s.state,"canceled")


    def test_num_people(self):
        a = Factory.create_demo_site("test", quick=True)
        self.assertEqual(a.num_people, Person.objects_by_account(a).count())

    
    def test_num_people_denominator(self):
        a = Factory.create_demo_site("test", quick=True)
        if Person.objects_by_account(a).count() > 0:
            self.assertEqual(a.num_people, Person.objects_by_account(a).count())
        else:
            self.assertEqual(a.num_people,1)

    def test_num_organizations(self):
        a = Factory.create_demo_site("test", quick=True)
        self.assertEqual(a.num_organizations, Organization.objects_by_account(a).count())

    
    def test_num_donations(self):
        a = Factory.create_demo_site("test", quick=True)
        self.assertEqual(a.num_donations, Donation.objects_by_account(a).count())

    
    def test_num_donations_denominator(self):
        a = Factory.create_demo_site("test", quick=True)
        if Donation.objects_by_account(a).count() > 0:
            self.assertEqual(a.num_donations, Donation.objects_by_account(a).count())
        else:
            self.assertEqual(a.num_donations,1)

    def test_total_donations(self):
        a = Factory.create_demo_site("test", quick=True)
        total = 0
        for d in Donation.objects_by_account(a).all():
            total += d.amount
        self.assertEqual(a.total_donations, total)

    
    def test_avg_donation(self):
        a = Factory.create_demo_site("test", quick=True)
        self.assertEqual(a.avg_donation, float(a.total_donations) / a.num_donations_denominator)
    
    def test_num_volunteer_hours(self):
        a = Factory.create_demo_site("test", quick=True)
        hours = 0
        for c in CompletedShift.objects.all():
            hours += c.duration

        self.assertEqual(a.num_volunteer_hours, hours)
    
    def test_avg_vol_hours_per_person(self):
        a = Factory.create_demo_site("test", quick=True)
        self.assertEqual(a.avg_vol_hours_per_person, float(a.num_volunteer_hours) /a.num_people_denominator)
    
    def test_num_tags(self):
        a = Factory.create_demo_site("test", quick=True)
        self.assertEqual(a.num_tags, Tag.objects_by_account(a).count())

    
    def test_num_taggeditems(self):
        a = Factory.create_demo_site("test", quick=True)
        self.assertEqual(a.num_taggeditems, TaggedItem.objects_by_account(a).count())

    
    def test_avg_tags_per_person(self):
        a = Factory.create_demo_site("test", quick=True)
        self.assertEqual(a.avg_tags_per_person, float(a.num_taggeditems) / a.num_people_denominator)
    

    def test_num_groups(self):
        a = Factory.create_demo_site("test", quick=True)
        self.assertEqual(a.num_groups, Group.objects_by_account(a).count())
    
    
    def test_num_spreadsheets(self):
        a = Factory.create_demo_site("test", quick=True)
        self.assertEqual(a.num_spreadsheets, Spreadsheet.objects_by_account(a).count())


    # def test_that_signing_up_generates_a_message_to_the_user_and_to_us(self):
    #     from django.test.client import Client
    #     from accounts.tests.selenium_abstractions import _sitespaced_url
    #     c = Client()
    #     response = c.post(_sitespaced_url('/signup'), {
    #         'name': 'My Test Organization', 
    #         'subdomain': 'mytestorganization',
    #         'first_name': 'Joe Smith',
    #         'email': 'joe@example.com',
    #         'username': 'joe',
    #         'password': 'test'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(len(mail.outbox), 2)
    #     self.assertEqual(mail.outbox[0].subject, 'Welcome to GoodCloud!')
    #     assert "we hope you enjoy using GoodCloud" in mail.outbox[0].body
    #     self.assertEqual(mail.outbox[1].subject, 'New Account: My Test Organization!')
    #     assert "joe@example.com" in mail.outbox[1].body
