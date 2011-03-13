# encoding: utf-8
from djangosanetesting.cases import SeleniumTestCase
import time 
from test_factory import Factory
from django.core.management import call_command
from people.tests.selenium_tests import PeopleTestAbstractions
from django.contrib.humanize.templatetags.humanize import naturalday

class DonorTestAbstractions(object):

    def create_person_and_go_to_donor_tab(self):
        sel = self.selenium
        self.create_john_smith()
        self.switch_to_donor_tab()
    
    def create_person_with_one_donation(self):
        sel = self.selenium
        self.create_person_and_go_to_donor_tab()
        return self.add_a_donation()

    def switch_to_donor_tab(self):
        sel = self.selenium
        sel.click("css=.detail_tab[href=#donor]")
        time.sleep(1)


    def add_a_donation(self, amount=None, date=None):
        sel = self.selenium
        self.switch_to_donor_tab()
        if not amount:
            amount = "%.2f" % (Factory.rand_currency())
        if not date:
            d = Factory.rand_date()
            date = "%.2f/%.2f/%.2f" % (d.month, d.day, d.year)
        sel.click("css=tabbed_box[name=add_a_donation] tab_title")
        sel.type("css=#id_amount", amount)
        sel.type("css=#id_date", date)
        sel.click("css=tabbed_box[name=add_a_donation] .add_donation_btn")
        time.sleep(2)
        return amount,date

class TestAgainstNoData(SeleniumTestCase, DonorTestAbstractions, PeopleTestAbstractions):
    def setUp(self):
        self.verificationErrors = []
    
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)
        call_command('flush', interactive=False)

    def test_that_new_donations_can_be_added_and_display_properly(self):
        sel = self.selenium        
        self.create_person_and_go_to_donor_tab()
        a1, d1 = self.add_a_donation(amount=85.12, date="3/12/2011")
        a2, d2 = self.add_a_donation(amount=12.15, date="1/4/2011")
        a3, d3 = self.add_a_donation(amount=8.04, date="10/17/2010")

        # make sure recent donations display cleanly
        self.assertEqual("$%.2f"%a1, sel.get_text("css=.donor_donation_table .donation_row:nth(0) .amount"))
        self.assertEqual("March 12, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .date"))

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
        # self.assertEqual("March 12, 2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_donor_donations_table .donation_row:nth(0) .date"))

        # self.assertEqual("$%.2f"%a2, sel.get_text("css=.year_of_shifts:nth(0) .year_of_donor_donations_table .donation_row:nth(1) .amount"))
        # self.assertEqual("Jan. 4, 2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_donor_donations_table .donation_row:nth(1) .date"))
        
        # self.assertEqual("$%.2f"%a3, sel.get_text("css=.year_of_shifts:nth(1) .year_of_donor_donations_table .donation_row .amount"))
        # self.assertEqual("Oct. 17, 2010", sel.get_text("css=.year_of_shifts:nth(1) .year_of_donor_donations_table .donation_row .date"))
   
    def test_that_donations_are_rounded_to_cents(self):
        sel = self.selenium
        self.create_person_and_go_to_donor_tab()
        a1, d1 = self.add_a_donation(amount=87.12511546123, date="3/12/2011")

        # because jquery datepicker + selenium argue.
        self.switch_to_donor_tab()
        # make sure recent donations display cleanly
        self.assertEqual("$87.13", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .amount"))
        self.assertEqual("March 12, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .date"))

    def test_that_deleting_donation_works(self):
        sel = self.selenium        
        self.create_person_with_one_donation()
        a1, d1 = self.add_a_donation(amount=85.12, date="3/12/2011")
        a2, d2 = self.add_a_donation(amount=12.15, date="1/4/2011")        

        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.donor_donation_table .donation_row:nth(1) .delete_donation_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to remove this donation?\n\nPress OK to remove the donation.\nPress Cancel to leave things as-is.")
        self.assertEqual("$%.2f"%a1, sel.get_text("css=.donor_donation_table .donation_row:nth(0) .amount"))
        self.assertEqual("March 12, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .date"))

        self.assertEqual("$%.2f"%a2, sel.get_text("css=.donor_donation_table .donation_row:nth(1) .amount"))
        self.assertEqual("Jan. 4, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(1) .date"))

        sel.click("css=.donor_donation_table .donation_row:nth(1) .delete_donation_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to remove this donation?\n\nPress OK to remove the donation.\nPress Cancel to leave things as-is.")

        time.sleep(5)
        self.assertEqual("$%.2f"%a1, sel.get_text("css=.donor_donation_table .donation_row:nth(0) .amount"))
        self.assertEqual("March 12, 2011", sel.get_text("css=.donor_donation_table .donation_row:nth(0) .date"))

    def test_people_can_have_tags_added_and_removed_and_the_results_stick(self):
        sel = self.selenium
        self.create_person_and_go_to_donor_tab()
        time.sleep(5)        
        self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        self.assertEqual("Saved", sel.get_text("css=.save_and_status_btn"))
        sel.click("link=Done")
        time.sleep(1)        
        
        sel.click("css=.tags_and_other_info tag.new_tag input[name=new_tag]")
        sel.type("css=.tags_and_other_info tag.new_tag input[name=new_tag]","Volunteer")
        sel.click("css=.tags_and_other_info tag.new_tag .tag_add_btn")
        time.sleep(2)
        self.assertEqual("volunteer",sel.get_text("css=.tags_and_other_info tags tag:nth(0) name"))

        sel.click("css=.tags_and_other_info tag.new_tag input[name=new_tag]")
        sel.type("css=.tags_and_other_info tag.new_tag input[name=new_tag]","Major Donor")
        sel.click("css=.tags_and_other_info tag.new_tag .tag_add_btn")
        time.sleep(2)
        # Alphabetical order checked
        self.assertEqual("major donor",sel.get_text("css=.tags_and_other_info tags tag:nth(0) name"))
        self.assertEqual("volunteer",sel.get_text("css=.tags_and_other_info tags tag:nth(1) name"))

        sel.click("css=.tags_and_other_info tag.new_tag input[name=new_tag]")
        sel.type("css=.tags_and_other_info tag.new_tag input[name=new_tag]","mistake tag")
        sel.click("css=.tags_and_other_info tag.new_tag .tag_add_btn")
        time.sleep(2)
        self.assertEqual("major donor",sel.get_text("css=.tags_and_other_info tags tag:nth(0) name"))
        self.assertEqual("mistake tag",sel.get_text("css=.tags_and_other_info tags tag:nth(1) name"))
        self.assertEqual("volunteer",sel.get_text("css=.tags_and_other_info tags tag:nth(2) name"))

        sel.click("css=.tags_and_other_info tags tag:nth(1) .remove_tag_link")      
        time.sleep(2)
        self.assertEqual("major donor",sel.get_text("css=.tags_and_other_info tags tag:nth(0) name"))
        self.assertEqual("volunteer",sel.get_text("css=.tags_and_other_info tags tag:nth(1) name"))

        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.switch_to_donor_tab()
        self.assertEqual("major donor",sel.get_text("css=.tags_and_other_info tags tag:nth(0) name"))
        self.assertEqual("volunteer",sel.get_text("css=.tags_and_other_info tags tag:nth(1) name"))

    def test_people_can_see_and_select_previous_tags_via_autocomplete(self):
        sel = self.selenium
        sel.open("/people/search")
        self.create_person_and_go_to_donor_tab()
        time.sleep(5)        
        self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        self.assertEqual("Saved", sel.get_text("css=.save_and_status_btn"))
        sel.click("link=Done")
        time.sleep(1)        

        sel.click("css=.tags_and_other_info tag.new_tag input[name=new_tag]")
        sel.type("css=.tags_and_other_info tag.new_tag input[name=new_tag]","monthly donor")
        sel.click("css=.tags_and_other_info tag.new_tag .tag_add_btn")
        time.sleep(2)
        # because jquery datepicker + selenium argue.
        self.switch_to_donor_tab()        
        
        self.assertEqual("monthly donor",sel.get_text("css=.tags_and_other_info tags tag:nth(0) name"))
        sel.click("css=.tags_and_other_info tag.new_tag input[name=new_tag]")
        sel.type("css=.tags_and_other_info tag.new_tag input[name=new_tag]","Major Donor")
        sel.click("css=.tags_and_other_info tag.new_tag .tag_add_btn")
        time.sleep(2)
        sel.click("css=.tags_and_other_info tag.new_tag input[name=new_tag]")
        sel.type("css=.tags_and_other_info tag.new_tag input[name=new_tag]","mistake tag")
        sel.click("css=.tags_and_other_info tag.new_tag .tag_add_btn")
        time.sleep(2)

        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.click("link=New Person")
        sel.wait_for_page_to_load("30000")
        sel.type("id_first_name", "Joe")
        sel.type("id_last_name", "Williams")
        self.switch_to_donor_tab()
        sel.click("css=.tags_and_other_info tag.new_tag input[name=new_tag]")
        sel.type("css=.tags_and_other_info tag.new_tag input[name=new_tag]","M")
        time.sleep(2)
        assert sel.is_element_present("css=.new_tag_list .tag_suggestion_link")
        self.assertEqual("major donor",sel.get_text("css=.new_tag_list .tag_suggestion_link:nth(0)"))
        self.assertEqual("mistake tag",sel.get_text("css=.new_tag_list .tag_suggestion_link:nth(1)"))
        sel.click("css=.tags_and_other_info tag.new_tag input[name=new_tag]")
        sel.type("css=.tags_and_other_info tag.new_tag input[name=new_tag]","")
        time.sleep(1)
        assert not sel.is_element_present("css=.new_tag_list .tag_suggestion_link")

        sel.click("css=.tags_and_other_info tag.new_tag input[name=new_tag]")
        sel.type("css=.tags_and_other_info tag.new_tag input[name=new_tag]","Ma")
        time.sleep(1)
        assert sel.is_element_present("css=.new_tag_list .tag_suggestion_link")
        self.assertEqual("major donor",sel.get_text("css=.new_tag_list .tag_suggestion_link:nth(0)"))
        sel.click("css=.new_tag_list .tag_suggestion_link:nth(0)")
        time.sleep(1)
        self.assertEqual(sel.get_value("css=.tags_and_other_info tag.new_tag input[name=new_tag]"), "major donor")
        sel.click("css=.tags_and_other_info tag.new_tag .tag_add_btn")
        time.sleep(1)
        self.assertEqual("major donor",sel.get_text("css=.tags_and_other_info tags tag:nth(0) name"))


class TestAgainstGeneratedData(SeleniumTestCase, DonorTestAbstractions, PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    
    def tearDown(self,*args, **kwargs):
        call_command('flush', interactive=False)
        self.assertEqual([], self.verificationErrors)



