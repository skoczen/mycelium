import time
from test_factory import Factory


class DonorTestAbstractions(object):

    def create_person_and_go_to_donor_tab(self):
        self.create_john_smith()
        self.switch_to_donor_tab()
    
    def create_person_with_one_donation(self):
        self.create_person_and_go_to_donor_tab()
        return self.add_a_donation()

    def switch_to_donor_tab(self):
        sel = self.selenium
        sel.click("css=.detail_tab[href=#donor]")
        time.sleep(1)


    def add_a_donation(self, amount=None, date=None, type=None, notes=None, in_honor=False, in_memory=False, honorarium_name=None):
        sel = self.selenium
        self.switch_to_donor_tab()
        if not amount:
            amount = "%.2f" % (Factory.rand_currency())
        if not date:
            d = Factory.rand_date()
            date = "%02d/%02d/%02d" % (d.month, d.day, d.year)
        sel.click("css=tabbed_box[name=add_a_donation] tab_title")
        sel.type("css=#id_amount", amount)
        sel.type("css=#id_date", date)
        if type:
            sel.select("css=#id_type",type)
        if notes:
            sel.type("css=#id_notes", notes)

        if in_honor:
            sel.click("css=#id_in_honor_of")
        
        if in_memory:
            sel.click("css=#id_in_memory_of")
        
        if honorarium_name:
            sel.type("css=#id_honorarium_name", honorarium_name)

        sel.click("css=tabbed_box[name=add_a_donation] .add_donation_btn")
        time.sleep(2)
        return amount,date