# encoding: utf-8
from djangosanetesting.cases import SeleniumTestCase
import time 
from test_factory import Factory
from django.core.management import call_command
from people.tests.selenium_tests import PeopleTestAbstractions

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

class TestAgainstNoData(SeleniumTestCase,VolunteerTestAbstractions,PeopleTestAbstractions):
    def setUp(self):
        self.verificationErrors = []
    
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)
        call_command('flush', interactive=False)


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



class TestAgainstGeneratedData(SeleniumTestCase,VolunteerTestAbstractions,PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    
    def tearDown(self,*args, **kwargs):
        call_command('flush', interactive=False)
        self.assertEqual([], self.verificationErrors)


    def test_create_new_volunteer(self):
        self.create_new_volunteer()

