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
        self.a1 = self.create_demo_site(with_demo_flag=False)
        self.create_demo_site(name="test1")
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
        self.assertEqual(sel.get_text("css=.num_people number") , "%s" % (Person.objects.non_demo.count() / Account.objects.active.count()))

    def test_that_flight_control_lists_the_right_organizations_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        self.assertEqual(sel.get_text("css=.num_orgs number") , "%s" % (Organization.objects.non_demo.count() / Account.objects.active.count()))

    def test_that_flight_control_lists_the_right_users_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        self.assertEqual(sel.get_text("css=.num_users number") , "%.1f" % (UserAccount.objects.non_demo.count() / Account.objects.active.count()))

    def test_that_flight_control_lists_the_right_donations_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        self.assertEqual(sel.get_text("css=.num_donations number") , "%.1f" % (Donation.objects.non_demo.count() / Account.objects.active.count()))

    def test_that_flight_control_lists_the_right_per_donation_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        total_donations = 0
        for d in Donation.objects.non_demo.all():
            total_donations += d.amount
        self.assertEqual(sel.get_text("css=.num_donations number") , "%.1f" % (total_donations / Donation.objects.non_demo.count()))


    def test_that_flight_control_lists_the_right_vol_hours_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        total_volunteer_hours = 0
        for cs in CompletedShift.objects.non_demo.all():
            total_volunteer_hours += cs.duration
        self.assertEqual(sel.get_text("css=.num_vol_hours number") , "%.1f" % (total_volunteer_hours / Person.objects.non_demo.count()))

    def test_that_flight_control_lists_the_right_per_Completed_shift_average(self):
        sel = self.selenium
        self.get_to_flight_control()
        total_volunteer_hours = 0
        for cs in CompletedShift.objects.non_demo.all():
            total_volunteer_hours += cs.duration
        self.assertEqual(sel.get_text("css=.avg_vol_hours_per_person number") , "%.1f" % (total_volunteer_hours / Account.objects.active.count()))


    def test_that_flight_control_lists_accounts_that_expire_soon(self):
        sel = self.selenium
        self.get_to_flight_control()
        assert sel.is_text_present("None in the next week.")
        a = self.a1
        a.signup_date = datetime.datetime.now() - datetime.timedelta(days=25)
        a.save()
        cache.clear()
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert not sel.is_text_present("None in the next week.")



    def test_that_each_week_displays_correctly(self):
        sel = self.selenium
        self.get_to_flight_control()
        a = self.a1
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(0) span:nth(0)"),"1")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(1) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(2) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(3) span:nth(0)"),"0")
        a.signup_date = datetime.datetime.now() - datetime.timedelta(days=12)
        a.save()
        cache.clear()
        sel.refresh()
        sel.wait_for_page_to_load("30000")

        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(0) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(1) span:nth(0)"),"1")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(2) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(3) span:nth(0)"),"0")
        a.signup_date = datetime.datetime.now() - datetime.timedelta(days=18)
        a.save()
        cache.clear()
        sel.refresh()
        sel.wait_for_page_to_load("30000")

        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(0) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(1) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(2) span:nth(0)"),"1")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(3) span:nth(0)"),"0")
        a.signup_date = datetime.datetime.now() - datetime.timedelta(days=25)
        a.save()
        cache.clear()
        sel.refresh()
        sel.wait_for_page_to_load("30000")

        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(0) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(1) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(2) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(3) span:nth(0)"),"1")
        a.signup_date = datetime.datetime.now() - datetime.timedelta(days=35)
        a.save()
        cache.clear()
        sel.refresh()
        sel.wait_for_page_to_load("30000")

        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(0) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(1) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(2) span:nth(0)"),"0")
        self.assertEqual(sel.get_text("css=.free_trial .flip.bottom:nth(3) span:nth(0)"),"0")


    def test_that_the_number_of_active_accounts_displays_correctly(self):
        sel = self.selenium
        self.get_to_flight_control()
        self.assertEqual(sel.get_text("css=.active .flip.bottom:nth(0) span:nth(0)"),"1")


    def test_that_accounts_with_billing_issues_display(self):
        sel = self.selenium
        self.get_to_flight_control()
        assert sel.is_text_present("No accounts with billing issues! Hooray!")
        self.assertEqual(sel.get_text("css=.billing .flip.bottom:nth(0) span:nth(0)"),"0")
        a = self.a1
        a.status = 10
        a.save()
        cache.clear()
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert not sel.is_text_present("No accounts with billing issues! Hooray!")
        assert sel.is_text_present("test is Expired")
        self.assertEqual(sel.get_text("css=.billing .flip.bottom:nth(0) span:nth(0)"),"1")
    
    def test_searching_for_an_account_works(self):
        self.get_to_flight_control()
        self.get_to_account_by_searching()

    def test_account_page_displays_the_correct_number_of_people(self):
        sel = self.selenium
        self.get_to_flight_control()
        self.get_to_account_by_searching()
        self.assertEqual(sel.get_text("css=.num_people number"), "%s" % self.a1.num_people)


class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, FlightControlTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
