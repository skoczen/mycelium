import time
from test_factory import Factory

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
        # self.assertEqual("on an unscheduled shift.", sel.get_text("css=.volunteer_shift_table:nth(0) .completed_volunteer_shift_row .shift"))
        self.assertEqual("2011", sel.get_text("css=.year_overview:nth(0) .year"))
        self.assertEqual("1 shift", sel.get_text("css=.year_overview:nth(0) .total_shifts"))
        self.assertEqual("4 hours", sel.get_text("css=.year_overview:nth(0) .total_hours"))
        sel.click("link=See details")
        self.assertEqual("4 hours", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .duration"))
        self.assertEqual("Feb. 11, 2011", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .date"))
        # self.assertEqual("on an unscheduled shift.", sel.get_text("css=.year_of_shifts:nth(0) .year_of_volunteer_shifts_table .completed_volunteer_shift_row .shift"))
    

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