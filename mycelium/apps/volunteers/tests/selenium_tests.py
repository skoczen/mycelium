# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time 
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from accounts.tests.selenium_abstractions import AccountTestAbstractions

class VolunteerTestAbstractions(object):

    def create_new_volunteer(self):
        sel = self.selenium
        self.create_john_smith_and_verify()
        sel.click("css=.detail_tab[href=#volunteer]")
        time.sleep(1)
        assert sel.is_text_present("No volunteer shifts yet")
    
    def create_new_volunteer_with_one_shift(self):
        sel = self.selenium
        self.create_new_volunteer()
        sel.click("css=.detail_tab[href=#volunteer]")
        time.sleep(1)
        assert sel.is_text_present("No volunteer shifts yet")
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] tab_title")
        sel.type("css=#id_duration", 4)
        sel.type("css=#id_date", "2/11/2011")
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] .add_shift_btn")
        time.sleep(1)        


        self.assertEqual("4 hours", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .duration"))
        self.assertEqual("Feb. 11, 2011", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .shift"))
        self.assertEqual("2011", sel.get_text("css=.year_overview:nth(0) .year"))
        self.assertEqual("1 shift", sel.get_text("css=.year_overview:nth(0) .total_shifts"))
        self.assertEqual("4 hours", sel.get_text("css=.year_overview:nth(0) .total_hours"))
        sel.click("link=See details")
        self.assertEqual("4 hours", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("Feb. 11, 2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .shift"))
    

    def add_a_new_shift(self, hours=None, date=None):
        sel = self.selenium
        if not hours:
            hours = Factory.rand_int(1,10)

        sel.click("css=tabbed_box[name=add_a_volunteer_shift] tab_title")
        sel.type("css=#id_duration", hours)
        if date:
            sel.type("css=#id_date", date)
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] .add_shift_btn")
        time.sleep(2)

class TestAgainstNoData(QiConservativeSeleniumTestCase,VolunteerTestAbstractions,PeopleTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_tests()
        self.verificationErrors = []


    def test_create_new_volunteer(self):
        self.create_new_volunteer()

    def test_create_new_volunteer_with_one_shift(self):
        self.create_new_volunteer_with_one_shift()

    def test_add_several_shifts_to_one_volunteer_and_verify_they_display(self):
        sel = self.selenium        
        self.create_new_volunteer_with_one_shift()

        sel.click("css=tabbed_box[name=add_a_volunteer_shift] tab_title")
        sel.type("css=#id_duration", 8)
        sel.type("css=#id_date", "1/14/2011")
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] .add_shift_btn")
        time.sleep(2)        
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] tab_title")
        sel.type("css=#id_duration", 3.75)
        sel.type("css=#id_date", "12/28/2010")
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] .add_shift_btn")
        time.sleep(2)        

        # make sure recent shifts display cleanly
        self.assertEqual("4 hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("Feb. 11, 2011", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .shift"))

        self.assertEqual("8 hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .duration"))
        self.assertEqual("Jan. 14, 2011", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .shift"))
        
        self.assertEqual(u"3¾ hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(2) .duration"))
        self.assertEqual("Dec. 28, 2010", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(2) .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(2) .shift"))
                        

        self.assertEqual("2011", sel.get_text("css=.year_overview:nth(0) .year"))
        self.assertEqual("2 shifts", sel.get_text("css=.year_overview:nth(0) .total_shifts"))
        self.assertEqual("12 hours", sel.get_text("css=.year_overview:nth(0) .total_hours"))

        self.assertEqual("2010", sel.get_text("css=.year_overview:nth(1) .year"))
        self.assertEqual("1 shift", sel.get_text("css=.year_overview:nth(1) .total_shifts"))
        self.assertEqual(u"4 hours", sel.get_text("css=.year_overview:nth(1) .total_hours"))

        sel.click("link=See details")
        self.assertEqual("4 hours", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(0) .duration"))
        self.assertEqual("Feb. 11, 2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(0) .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(0) .shift"))

        self.assertEqual("8 hours", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(1) .duration"))
        self.assertEqual("Jan. 14, 2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(1) .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(1) .shift"))
        
        self.assertEqual(u"3¾ hours", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("Dec. 28, 2010", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .shift"))
        
    # TODO: Fix the jquery UI / selenium conflict, then enable this test.                
    # def test_that_the_datepicker_opens_when_adding_a_new_shift(self):
    #     sel = self.selenium
    #     self.create_new_volunteer()
        
    #     sel.click("css=tabbed_box[name=add_a_volunteer_shift] tab_title")
    #     time.sleep(1)
    #     sel.click_at("css=#id_date", "5,5")
    #     sel.focus("css=#id_date")
    #     sel.set_cursor_position("css=#id_date",0)
    #     time.sleep(2)

    #     assert sel.is_element_present("css=#ui-datepicker-div")
    #     assert sel.is_visible("css=#ui-datepicker-div")

    def test_that_shifts_are_rounded_to_the_nearest_quarter_hour(self):
        sel = self.selenium
        self.create_new_volunteer()
        
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] tab_title")
        sel.type("css=#id_duration", "3.3")
        sel.type("css=#id_date", "12/28/2010")
        time.sleep(0.25)
        self.assertEqual(sel.get_value("css=#id_duration"),"3.25")

        sel.type("css=#id_duration", "12.024641564")
        sel.type("css=#id_date", "12/28/2010")
        time.sleep(0.25)
        self.assertEqual(sel.get_value("css=#id_duration"),"12")

        sel.type("css=#id_duration", "5.55")
        sel.type("css=#id_date", "12/28/2010")
        time.sleep(0.25)
        self.assertEqual(sel.get_value("css=#id_duration"),"5.5")


        sel.click("css=tabbed_box[name=add_a_volunteer_shift] .add_shift_btn")
        time.sleep(2)     

        self.assertEqual(u"5½ hours", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .duration"))
        self.assertEqual("Dec. 28, 2010", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .shift"))
        self.assertEqual("2010", sel.get_text("css=.year_overview:nth(0) .year"))
        self.assertEqual("1 shift", sel.get_text("css=.year_overview:nth(0) .total_shifts"))
        self.assertEqual(u"6 hours", sel.get_text("css=.year_overview:nth(0) .total_hours"))

    def test_that_shifts_are_rounded_to_the_nearest_quarter_hour_even_if_submitted_oddly(self):
        sel = self.selenium
        self.create_new_volunteer()
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] tab_title")        
        sel.type("css=#id_duration", "5.55")
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] .add_shift_btn")
        time.sleep(2)     

        self.assertEqual(u"5½ hours", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .duration"))
        self.assertEqual("today", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .shift"))
        self.assertEqual("2011", sel.get_text("css=.year_overview:nth(0) .year"))
        self.assertEqual("1 shift", sel.get_text("css=.year_overview:nth(0) .total_shifts"))
        self.assertEqual(u"6 hours", sel.get_text("css=.year_overview:nth(0) .total_hours"))


    def test_that_deleting_shifts_works(self):
        sel = self.selenium        
        self.create_new_volunteer_with_one_shift()

        sel.click("css=tabbed_box[name=add_a_volunteer_shift] tab_title")
        sel.type("css=#id_duration", 8)
        sel.type("css=#id_date", "1/14/2011")
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] .add_shift_btn")
        time.sleep(2)        
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] tab_title")
        sel.type("css=#id_duration", 3.75)
        sel.type("css=#id_date", "12/28/2010")
        sel.click("css=tabbed_box[name=add_a_volunteer_shift] .add_shift_btn")
        time.sleep(2)        

        # make sure recent shifts display cleanly
        self.assertEqual("4 hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("Feb. 11, 2011", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .shift"))

        self.assertEqual("8 hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .duration"))
        self.assertEqual("Jan. 14, 2011", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .shift"))
        
        self.assertEqual(u"3¾ hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(2) .duration"))
        self.assertEqual("Dec. 28, 2010", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(2) .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(2) .shift"))
                        

        self.assertEqual("2011", sel.get_text("css=.year_overview:nth(0) .year"))
        self.assertEqual("2 shifts", sel.get_text("css=.year_overview:nth(0) .total_shifts"))
        self.assertEqual("12 hours", sel.get_text("css=.year_overview:nth(0) .total_hours"))

        self.assertEqual("2010", sel.get_text("css=.year_overview:nth(1) .year"))
        self.assertEqual("1 shift", sel.get_text("css=.year_overview:nth(1) .total_shifts"))
        self.assertEqual(u"4 hours", sel.get_text("css=.year_overview:nth(1) .total_hours"))

        sel.click("link=See details")
        self.assertEqual("4 hours", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(0) .duration"))
        self.assertEqual("Feb. 11, 2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(0) .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(0) .shift"))

        self.assertEqual("8 hours", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(1) .duration"))
        self.assertEqual("Jan. 14, 2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(1) .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row:nth(1) .shift"))
        
        self.assertEqual(u"3¾ hours", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("Dec. 28, 2010", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .shift"))

        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .delete_shift_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to remove this shift?\n\nPress OK to remove the shift.\nPress Cancel to leave things as-is.")
        self.assertEqual("4 hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("Feb. 11, 2011", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .shift"))

        self.assertEqual("8 hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .duration"))
        self.assertEqual("Jan. 14, 2011", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .shift"))
        
        self.assertEqual(u"3¾ hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(2) .duration"))
        self.assertEqual("Dec. 28, 2010", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(2) .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(2) .shift"))

        sel.click("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .delete_shift_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to remove this shift?\n\nPress OK to remove the shift.\nPress Cancel to leave things as-is.")
        time.sleep(5)
        self.assertEqual("4 hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("Feb. 11, 2011", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .shift"))

        self.assertEqual(u"3¾ hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .duration"))
        self.assertEqual("Dec. 28, 2010", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row:nth(1) .shift"))

    def test_changing_status(self):
        sel = self.selenium
        self.create_new_volunteer()
        time.sleep(1)
        sel.click("css=.status_field label[for$=status_1]")
        sel.click("css=.status_field input[id$=status_1]")
        time.sleep(5)
        self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))

        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.detail_tab[href=#volunteer]")
        time.sleep(1)
        assert sel.is_element_present("css=.status_field input[id$=status_1]:checked")


        sel.click("css=.status_field label[for$=status_2]")
        time.sleep(0.25)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.detail_tab[href=#volunteer]")
        time.sleep(1)
        assert sel.is_element_present("css=.status_field input[id$=status_2]:checked")

        sel.click("css=.status_field label[for$=status_3]")
        time.sleep(1)
        sel.type("css=#id_VOLUNTEER_STATUS-reactivation_date", "01/2/2010")
        time.sleep(0.25)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.detail_tab[href=#volunteer]")
        time.sleep(1)
        assert sel.is_element_present("css=.status_field input[id$=status_3]:checked")
        self.assertEqual(sel.get_value("css=#id_VOLUNTEER_STATUS-reactivation_date"),"01/02/2010")



class TestAgainstGeneratedData(QiConservativeSeleniumTestCase,VolunteerTestAbstractions,PeopleTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_tests()
        self.people = [Factory.person(self.account) for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []


    def test_create_new_volunteer(self):
        self.create_new_volunteer()

