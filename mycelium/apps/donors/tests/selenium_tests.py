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
        self.assertEqual("Notes: %s" % notes_str, sel.get_text("css=.donor_donation_table .donation_row:nth(0) .notes_body"))



    def test_that_in_honorarium_fields_show_and_hide_properly(self):
        sel = self.selenium        
        self.create_person_and_go_to_donor_tab()
        self.switch_to_donor_tab()
        sel.click("css=tabbed_box[name=add_a_donation] tab_title")
        time.sleep(2)

        # check honor, make sure we have the name
        assert not sel.is_element_present("css=.honorarium_name")
        assert not sel.is_element_present("css=.in_honor_of .honorarium_name")
        sel.click("css=#id_in_honor_of")
        assert sel.is_element_present("css=.in_honor_of .honorarium_name")

        # uncheck, it goes away
        sel.click("css=#id_in_honor_of")
        assert not sel.is_element_present("css=.honorarium_name")
        assert not sel.is_element_present("css=.in_honor_of .honorarium_name")

        # check honor, then check memory, check for memory field
        sel.check("css=#id_in_honor_of")
        time.sleep(0.5)
        sel.click("css=#id_in_memory_of")
        time.sleep(0.5)
        assert sel.is_element_present("css=.honorarium_name")
        assert not sel.is_element_present("css=.in_honor_of .honorarium_name")
        assert sel.is_element_present("css=.in_memory_of .honorarium_name")

        # uncheck, it goes away
        sel.click("css=#id_in_memory_of")
        assert not sel.is_element_present("css=.honorarium_name")


    def test_that_new_donations_can_be_in_honor_or_memory_of_a_name(self):
        sel = self.selenium
        self.create_person_and_go_to_donor_tab()
        a1, d1 = self.add_a_donation(amount=85.8, date="3/8/2011", in_honor=True, honorarium_name="William Stafford")

        assert sel.is_element_present("css=.donor_donation_table .donation_row:nth(0) .notes_icon")
        self.assertEqual("In Honor of William Stafford", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .notes_body"))


        a2, d2 = self.add_a_donation(amount=24.75, date="4/8/2011", in_memory=True, honorarium_name="T.S. Eliot")

        assert sel.is_element_present("css=.donor_donation_table .donation_row:nth(0) .notes_icon")
        self.assertEqual("In Memory of T.S. Eliot", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .notes_body"))

class TestAgainstGeneratedData(DjangoFunctionalConservativeSeleniumTestCase, DonorTestAbstractions, PeopleTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
        self.people = [Factory.person(self.account) for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    
    # def tearDown(self):
    #     self.account.delete()
