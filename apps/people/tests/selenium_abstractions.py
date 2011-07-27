import time 
from test_factory import Factory

class PeopleTestAbstractions(object):

    def create_john_smith(self):
        sel = self.selenium
        self.open("/people")
        sel.wait_for_page_to_load("30000")
        sel.click("link=New Person")
        sel.wait_for_page_to_load("30000")
        sel.type("id_first_name", "John")
        sel.type("id_last_name", "Smith")
        sel.type("id_phone_number", "555-123-4567")
        sel.type("id_email", "john@smithfamily.com")
        sel.type("id_line_1", "123 Main St")
        sel.type("id_line_2", "Apt 27")
        sel.type("id_city", "Wilsonville")
        sel.type("id_state", "KY")
        sel.type("id_postal_code", "12345")
        

    def create_john_smith_and_verify(self):
        sel = self.selenium
        self.create_john_smith()
        time.sleep(6)
        self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        self.assertEqual("Saved", sel.get_text("css=.save_and_status_btn"))
        sel.click("link=Done")
        time.sleep(1)        
        self.assertEqual("John", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
        self.assertEqual("Smith", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
        self.assertEqual("555-123-4567", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
        self.assertEqual("john@smithfamily.com", sel.get_text("//span[@id='container_id_email']/span[1]"))
        self.assertEqual("123 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        self.assertEqual("Apt 27", sel.get_text("//span[@id='container_id_line_2']/span[1]"))
        self.assertEqual("Wilsonville", sel.get_text("//span[@id='container_id_city']/span[1]"))
        self.assertEqual("KY", sel.get_text("//span[@id='container_id_state']/span[1]"))
        self.assertEqual("12345", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))
        
    def create_john_smith_and_return_to_search(self):
        sel = self.selenium
        self.create_john_smith()
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")


    def save_a_birthday(self, birth_day="9", birth_month="April", birth_year="1980"):
        sel = self.selenium
        sel.select("css=#id_birth_month", birth_month)
        sel.type("css=#id_birth_day", birth_day)
        sel.type("css=#id_birth_year", birth_year)
        time.sleep(4)
