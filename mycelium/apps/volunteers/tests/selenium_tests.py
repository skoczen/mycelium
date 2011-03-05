from djangosanetesting.cases import SeleniumTestCase
import time 
from test_factory import Factory
from django.core.management import call_command
from people.tests.selenium_tests import PeopleTestAbstractions

class VolunteerTestAbstractions(object):

    def create_new_volunteer(self):
        sel = self.selenium
        self.create_john_smith()
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


        self.assertEqual("2 hours", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .duration"))
        self.assertEqual("2/11/2011", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .shift"))
        self.assertEqual("2011", sel.get_text("css=.year_overview:nth(0) .completed_volunteer_shift_row .year"))
        self.assertEqual("1 shift", sel.get_text("css=.year_overview:nth(0) .completed_volunteer_shift_row .total_shifts"))
        self.assertEqual("2 hours", sel.get_text("css=.year_overview:nth(0) .completed_volunteer_shift_row .total_hours"))
        sel.click("link=See details")
        self.assertEqual("2 hours", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("2/11/2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .shift"))
    




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

    def test_add_several_shifts_to_one_volunteer(self):
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
        self.assertEqual("2 hours", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("2/11/2011", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table .completed_volunteer_shift_row .shift"))

        self.assertEqual("8 hours", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("1/14/2011", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .shift"))
        
        self.assertEqual("3¾ hours", sel.get_text("css=.year_of_shifts:nth(2) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("12/28/2010", sel.get_text("css=.year_of_shifts:nth(2) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(2) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .shift"))
                        


        self.assertEqual("2011", sel.get_text("//div[@id='page']/detail_tab_contents/fragment/table[2]/tbody/tr[1]/td[1]"))
        self.assertEqual("1 shift", sel.get_text("//div[@id='page']/detail_tab_contents/fragment/table[2]/tbody/tr[1]/td[2]"))
        self.assertEqual("2 hours", sel.get_text("//div[@id='page']/detail_tab_contents/fragment/table[2]/tbody/tr[1]/td[3]"))
                
        sel.click("link=See details")
        self.assertEqual("2 hours", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("2/11/2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .shift"))

        self.assertEqual("8 hours", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("1/14/2011", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(1) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .shift"))
        
        self.assertEqual("3¾ hours", sel.get_text("css=.year_of_shifts:nth(2) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("12/28/2010", sel.get_text("css=.year_of_shifts:nth(2) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .date"))
        self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(2) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .shift"))
                        
            

class TestAgainstGeneratedData(SeleniumTestCase,VolunteerTestAbstractions,PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    
    def tearDown(self,*args, **kwargs):
        call_command('flush', interactive=False)
        self.assertEqual([], self.verificationErrors)


    def test_create_new_volunteer(self):
        self.create_new_volunteer()

