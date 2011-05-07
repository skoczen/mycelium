import time
import datetime
from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase
from groups.models import Group
from people.models import Person, Organization, Employee
from donors.models import Donor, Donation
from accounts.models import Account
from volunteers.models import Volunteer, CompletedShift
from generic_tags.models import TagSet, Tag, TaggedItem
from django.core import mail
from decimal import Decimal

class Dummy(object):
    pass

class TestDashboard(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase):
    # fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        pass

    def test_challenge_has_imported_contacts(self):
        assert True == "Test written"
        
    def test_challenge_has_set_up_tags(self):
        assert True == "Test written"
        
    def test_challenge_has_added_board(self):
        assert True == "Test written"
        
    def test_challenge_has_created_other_accounts(self):
        assert True == "Test written"
        
    def test_challenge_has_downloaded_spreadsheet(self):
        assert True == "Test written"
        
    def test_challenge_has_submitted_support(self):
        assert True == "Test written"
        
    def test_has_completed_all_challenges(self):
        assert True == "Test written"
        
    def test_has_completed_any_challenges(self):
        assert True == "Test written"
        

    def test_by_the_numbers_numbers(self):
        # test against hand-counted queries
        from dashboard.views import _account_numbers_dict
        a1 = Factory.create_demo_site("test1", quick=True)
        Factory.create_demo_site("test2", quick=True)

        nums = _account_numbers_dict(a1)

        start_of_this_year = datetime.date(month=1, day=1, year=datetime.date.today().year)
        
        # total_donations
        total_donations_hand_count = 0
        for d in Donation.objects.all():
            if d.account == a1 and d.date >= start_of_this_year:
                total_donations_hand_count += 1
        self.assertEqual(nums["total_donations"], total_donations_hand_count)
        

        # total_donors
        total_donors_hand_count = 0
        donors_list = []
        for d in Donation.objects.all():
            if d.account == a1 and d.date >= start_of_this_year:
                if d.donor not in donors_list:
                    total_donors_hand_count += 1
                    donors_list.append(d.donor)
        self.assertEqual(nums["total_donors"], total_donors_hand_count)


        # total donation amount
        total_donation_amount_hand_count = 0
        for d in Donation.objects.all():
            if d.account == a1 and d.date >= start_of_this_year:
                total_donation_amount_hand_count += d.amount

        self.assertEqual(nums["total_donation_amount"], total_donation_amount_hand_count)
        
        # average
        nums_avg = "%f" % nums["average_donation"]
        calc_avg = "%f" % (total_donation_amount_hand_count/total_donations_hand_count)
        nums_avg = nums_avg[:-2]
        calc_avg = calc_avg[:-2]
        self.assertEqual(nums_avg, calc_avg )   
        
        # total_volunteer_hours
        total_volunteer_hours_hand_count = 0
        for d in CompletedShift.objects.all():
            if d.account == a1 and d.date >= start_of_this_year:
                total_volunteer_hours_hand_count += d.duration

        self.assertEqual(nums["total_volunteer_hours"], total_volunteer_hours_hand_count)

        # total_people
        total_people = 0
        for d in Person.objects.all():
            if d.account == a1:
                total_people += 1

        self.assertEqual(nums["total_people"], total_people)

        # total_orgs
        total_orgs = 0
        for d in Organization.objects.all():
            if d.account == a1:
                total_orgs += 1

        self.assertEqual(nums["total_orgs"], total_orgs)

        # total_groups
        total_groups = 0
        for d in Group.objects.all():
            if d.account == a1:
                total_groups += 1

        self.assertEqual(nums["total_groups"], total_groups)

        # total_tags 
        total_tags = 0
        for d in Tag.objects.all():
            if d.account == a1:
                total_tags += 1

        self.assertEqual(nums["total_tags"], total_tags)

        # total_taggeditems
        total_taggeditems = 0
        for d in TaggedItem.objects.all():
            if d.account == a1:
                total_taggeditems += 1

        self.assertEqual(nums["total_taggeditems"], total_taggeditems)

