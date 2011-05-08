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
        self.a1 = Factory.create_demo_site("test1", quick=True, mostly_empty=True)

    def test_challenge_has_imported_contacts(self):
    # Expected fail
        self.a1.check_challenge_progress()
        assert self.a1.challenge_has_imported_contacts == True
        
    def test_challenge_has_set_up_tags(self):
        self.test_challenge_has_added_board()
        self.a1.check_challenge_progress()
        assert self.a1.challenge_has_set_up_tags == False
        Factory.tag_person(self.a1)
        self.a1.check_challenge_progress()
        assert self.a1.challenge_has_set_up_tags == True
        
    def test_challenge_has_added_board(self):
        Factory.tag(self.a1, name="Board of Directors")
        bg = Factory.group(self.a1,"board of directors")
        Factory.grouprule(self.a1, "have any tag that","contains","Board of Directors", group=bg)
        self.a1.check_challenge_progress()
        assert self.a1.challenge_has_added_board == True
        
    def test_challenge_has_created_other_accounts(self):
        Factory.useraccount(self.a1)
        self.a1.check_challenge_progress()
        assert self.a1.challenge_has_created_other_accounts == True
        
    def test_challenge_has_downloaded_spreadsheet(self):
    # Expected fail
        self.a1.check_challenge_progress()
        assert self.a1.challenge_has_downloaded_spreadsheet == True
        
    def test_challenge_has_submitted_support(self):
        self.a1.challenge_has_submitted_support = True
        self.a1.save()
        self.a1.check_challenge_progress()
        assert self.a1.challenge_has_submitted_support == True
        
    def test_challenge_has_added_a_donation(self):
        Factory.donation(account=self.a1)
        self.a1.check_challenge_progress()
        assert self.a1.challenge_has_added_a_donation == True

        
    def test_challenge_has_logged_volunteer_hours(self):
        p = Factory.person(self.a1)
        Factory.completed_volunteer_shift(p)
        self.a1.check_challenge_progress()
        assert self.a1.challenge_has_logged_volunteer_hours == True


    def test_has_completed_all_challenges(self):
    # Expected fail until all others succeed.
        self.test_challenge_has_imported_contacts()
        self.test_challenge_has_set_up_tags()
        self.test_challenge_has_added_board()
        self.test_challenge_has_created_other_accounts()
        self.test_challenge_has_downloaded_spreadsheet()
        # self.test_challenge_has_submitted_support()
        self.test_challenge_has_added_a_donation()
        self.test_challenge_has_logged_volunteer_hours()
        self.a1.check_challenge_progress()
        assert self.a1.has_completed_all_challenges == True
        
    def test_has_completed_any_challenges(self):
        self.test_challenge_has_created_other_accounts()
        self.a1.check_challenge_progress()
        assert self.a1.has_completed_any_challenges == True

    def test_by_the_numbers_numbers(self):
        # test against hand-counted queries
        from dashboard.views import _account_numbers_dict
        a1 = Factory.create_demo_site("test2", quick=True)

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

