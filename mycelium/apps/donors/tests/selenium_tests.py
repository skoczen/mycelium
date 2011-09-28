# encoding: utf-8
from functional_tests.selenium_test_case import DjangoFunctionalConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from donors.tests.selenium_abstractions import DonorTestAbstractions


class TestAgainstNoData(DjangoFunctionalConservativeSeleniumTestCase, DonorTestAbstractions, PeopleTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_with_no_data()

    # def tearDown(self):
    #     # self.account.delete()
    #     pass

    def test_that_new_donations_can_be_added_and_display_properly(self):
        sel = self.selenium        
        self.create_person_and_go_to_donor_tab()
        a1, d1 = self.add_a_donation(amount=85.8, date="3/8/2011")
        a2, d2 = self.add_a_donation(amount=8.15, date="1/4/2011")
        a3, d3 = self.add_a_donation(amount=8.04, date="10/17/2010")

        # make sure recent donations display cleanly
        self.assertEqual("$%.2f"%a1, sel.get_text("css=.donor_donation_table .donation_row:nth(0) .amount"))
        self.assertEqual("March 8, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .date"))

        self.assertEqual("$%.2f"%a2, sel.get_text("css=.donor_donation_table .donation_row:nth(1) .amount"))
        self.assertEqual("Jan. 4, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(1) .date"))

        self.assertEqual("$%.2f"%a3, sel.get_text("css=.donor_donation_table .donation_row:nth(2) .amount"))
        self.assertEqual("Oct. 17, 2010", sel.get_text("css=.donor_donation_table .donation_row:nth(2) .date"))
                        

        self.assertEqual("2011", sel.get_text("css=.year_overview:nth(0) .year"))
        self.assertEqual("2 donations", sel.get_text("css=.year_overview:nth(0) .total_number_of_donations"))
        self.assertEqual("totalling $%.2f" % (a1+a2), sel.get_text("css=.year_overview:nth(0) .total_donations"))

        self.assertEqual("2010", sel.get_text("css=.year_overview:nth(1) .year"))
        self.assertEqual("1 donation", sel.get_text("css=.year_overview:nth(1) .total_number_of_donations"))
        self.assertEqual("totalling $%.2f" % (a3), sel.get_text("css=.year_overview:nth(1) .total_donations"))

        # TODO: re-enable this once jquery + datepicker get along.
        # sel.click("link=See details")
        # self.assertEqual("$%.2f"%a1, sel.get_text("css=.year_of_shifts:nth(0) .year_of_donor_donations_table .donation_row:nth(0) .amount"))
        # self.assertEqual("March 8, 2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_donor_donations_table .donation_row:nth(0) .date"))

        # self.assertEqual("$%.2f"%a2, sel.get_text("css=.year_of_shifts:nth(0) .year_of_donor_donations_table .donation_row:nth(1) .amount"))
        # self.assertEqual("Jan. 4, 2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_donor_donations_table .donation_row:nth(1) .date"))
        
        # self.assertEqual("$%.2f"%a3, sel.get_text("css=.year_of_shifts:nth(1) .year_of_donor_donations_table .donation_row .amount"))
        # self.assertEqual("Oct. 17, 2010", sel.get_text("css=.year_of_shifts:nth(1) .year_of_donor_donations_table .donation_row .date"))
   
    def test_that_donations_are_rounded_to_cents(self):
        sel = self.selenium
        self.create_person_and_go_to_donor_tab()
        a1, d1 = self.add_a_donation(amount=87.1251154683, date="3/8/2011")

        # because jquery datepicker + selenium argue.
        self.switch_to_donor_tab()
        # make sure recent donations display cleanly
        self.assertEqual("$87.13", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .amount"))
        self.assertEqual("March 8, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .date"))

    def test_that_deleting_donation_works(self):
        sel = self.selenium        
        self.create_person_with_one_donation()
        a1, d1 = self.add_a_donation(amount=85.8, date="3/8/2011")
        a2, d2 = self.add_a_donation(amount=8.15, date="1/4/2011")        

        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.donor_donation_table .donation_row:nth(1) .delete_donation_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to remove this donation?\n\nPress OK to remove the donation.\nPress Cancel to leave things as-is.")
        self.assertEqual("$%.2f"%a1, sel.get_text("css=.donor_donation_table .donation_row:nth(0) .amount"))
        self.assertEqual("March 8, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .date"))

        self.assertEqual("$%.2f"%a2, sel.get_text("css=.donor_donation_table .donation_row:nth(1) .amount"))
        self.assertEqual("Jan. 4, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(1) .date"))

        sel.click("css=.donor_donation_table .donation_row:nth(1) .delete_donation_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to remove this donation?\n\nPress OK to remove the donation.\nPress Cancel to leave things as-is.")

        time.sleep(5)
        self.assertEqual("$%.2f"%a1, sel.get_text("css=.donor_donation_table .donation_row:nth(0) .amount"))
        self.assertEqual("March 8, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .date"))


    def test_that_new_donations_can_include_a_type_and_notes(self):
        sel = self.selenium        
        self.create_person_and_go_to_donor_tab()
        notes_str = Factory.rand_str()
        a1, d1 = self.add_a_donation(amount=85.8, date="3/8/2011", type="Check", notes=notes_str)

        # make sure recent donations display cleanly
        self.assertEqual("$%.2f"%a1, sel.get_text("css=.donor_donation_table .donation_row:nth(0) .amount"))
        self.assertEqual("March 8, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .date"))
        self.assertEqual("Check", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .type"))
        self.assertEqual(notes_str, sel.get_text("css=.donor_donation_table .donation_row:nth(0) .notes"))




class TestAgainstGeneratedData(DjangoFunctionalConservativeSeleniumTestCase, DonorTestAbstractions, PeopleTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
        self.people = [Factory.person(self.account) for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    
    # def tearDown(self):
    #     self.account.delete()
