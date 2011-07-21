# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
import datetime
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from organizations.tests.selenium_abstractions import OrganizationsTestAbstractions
from groups.tests.selenium_abstractions import GroupTestAbstractions
from flight_control.tests.selenium_abstractions import FlightControlTestAbstractions
from django.conf import settings
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from django.core.cache import cache
from django.template.defaultfilters import date

from accounts.models import Account, UserAccount
from accounts import BILLING_PROBLEM_STATII
from people.models import Person
from organizations.models import Organization
from donors.models import Donation
from volunteers.models import CompletedShift
from generic_tags.models import Tag, TaggedItem
from groups.models import Group
from spreadsheets.models import Spreadsheet
from django.contrib.auth.models import User


    
class TestAgainstNoData(QiConservativeSeleniumTestCase, FlightControlTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()
        self.create_demo_site()
        self.create_demo_site(with_demo_flag=False)
        cache.clear()
        self.create_fake_account_for_flight_control()
        self.verificationErrors = []

    def test_that_flight_control_loads(self):
        self.get_to_flight_control()

    def test_that_flight_control_doesnt_load_for_another_user(self):
        sel = self.selenium
        sel.open("http://flightcontrol.localhost:%s" % settings.LIVE_SERVER_PORT)
        sel.wait_for_page_to_load("30000")
        sel.type("css=#id_username", "test")
        sel.type("css=#id_password", "test")
        sel.click("css=input[type=submit]")
        sel.wait_for_page_to_load("30000")
        assert not sel.is_text_present("GoodCloud Flight Control")

    def test_that_flight_control_lists_the_right_people_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        self.assertEqual(sel.get_text("css=.num_people number") , "%s" % (Person.objects.filter(account__is_demo=False).count() / Account.objects.active.count()))

    def test_that_flight_control_lists_the_right_organizations_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        self.assertEqual(sel.get_text("css=.num_orgs number") , "%s" % (Organization.objects.filter(account__is_demo=False).count() / Account.objects.active.count()))

    def test_that_flight_control_lists_the_right_users_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        self.assertEqual(sel.get_text("css=.num_users number") , "%.1f" % (UserAccount.objects.filter(account__is_demo=False).count() / Account.objects.active.count()))

    def test_that_flight_control_lists_the_right_donations_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        self.assertEqual(sel.get_text("css=.num_donations number") , "%.1f" % (Donation.objects.filter(account__is_demo=False).count() / Account.objects.active.count()))

    def test_that_flight_control_lists_the_right_per_donation_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        total_donations = 0
        for d in Donation.objects.filter(account__is_demo=False).all():
            total_donations += d.amount
        self.assertEqual(sel.get_text("css=.num_donations number") , "%.1f" % (total_donations / Account.objects.active.count()))


    def test_that_flight_control_lists_the_right_vol_hours_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        total_volunteer_hours = 0
        for cs in CompletedShift.objects.filter(account__is_demo=False).all():
            total_volunteer_hours += cs.duration
        self.assertEqual(sel.get_text("css=.num_vol_hours number") , "%.1f" % (total_volunteer_hours / Person.objects.filter(account__is_demo=False).count()))

    def testShat_flight_control_lists_the_right_per_Completed_shift_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        total_volunteer_hours = 0
        for cs in CompletedShift.objects.filter(account__is_demo=False).all():
            total_volunteer_hours += cs.duration
        self.assertEqual(sel.get_text("css=.avg_vol_hours_per_person number") , "%.1f" % (total_volunteer_hours / Account.objects.active.count()))




class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, FlightControlTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
