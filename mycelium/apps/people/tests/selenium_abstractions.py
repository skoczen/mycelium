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


    def create_new_organization(self):
        sel = self.selenium
        self.open("/people/")
        sel.click("link=New Organization")
        sel.wait_for_page_to_load("30000")
        sel.type("id_name", "Test Organization")
        sel.type("id_primary_phone_number", "555 123-4567")
        sel.type("id_website", "example.com")
        sel.type("id_twitter_username", "testorg")
        sel.type("id_line_1", "123 1st St")
        sel.type("id_line_2", "#125")
        sel.type("id_city", "Williamsburg")
        sel.type("id_state", "OH")
        sel.type("id_postal_code", "54321")
        time.sleep(3)
        sel.click("link=Done")
        self.assertEqual("Test Organization", sel.get_text("//span[@id='container_id_name']/span[1]"))
        self.assertEqual("555 123-4567", sel.get_text("//span[@id='container_id_primary_phone_number']/span[1]"))
        self.assertEqual("example.com", sel.get_text("//span[@id='container_id_website']/span[1]"))
        self.assertEqual("testorg", sel.get_text("//span[@id='container_id_twitter_username']/span[1]"))
        self.assertEqual("123 1st St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        self.assertEqual("#125", sel.get_text("//span[@id='container_id_line_2']/span[1]"))
        self.assertEqual("Williamsburg", sel.get_text("//span[@id='container_id_city']/span[1]"))
        self.assertEqual("OH", sel.get_text("//span[@id='container_id_state']/span[1]"))
        self.assertEqual("54321", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))
        
    def create_new_organization_with_employee(self):
        sel = self.selenium
        self.create_my_new_org()
        sel.click("css=tabbed_box tab_title")
        time.sleep(0.5)
        sel.click("id_search_new_person")
        sel.type("id_search_new_person", "Joyellen Smith")
        sel.click("link=Add a New Person")
        sel.click("css=#new_person form input[id$=role]")
        sel.type("css=#new_person form input[id$=role]", "Chief Tester")
        sel.type("css=#new_person form input[id$=email]", "joesmith@myneworg.org")
        sel.type("css=#new_person form input[id$=phone_number]", "503-247.8451")
        sel.click("//div[@id='new_person']/form/form_actions/input")
        time.sleep(2)
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Joyellen Smith", sel.get_text("link=Joyellen Smith"))
        self.assertEqual("Chief Tester", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("503-247.8451", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("joesmith@myneworg.org", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=email] .view_field"))        
        sel.click("css=tabbed_box tab_title")
        sel.click("css=tabbed_box box_close a")

    def create_new_organization_and_return_to_search(self):
        sel = self.selenium
        self.create_new_organization()
        sel.click("link=Back to All People and Organizations")
        sel.wait_for_page_to_load("30000")        


    def create_my_new_organization_with_employee_and_return_to_search(self):
        sel = self.selenium
        self.create_new_organization_with_employee()
        sel.click("link=Back to All People and Organizations")
        sel.wait_for_page_to_load("30000")        


    def save_a_birthday(self, birth_day="9", birth_month="April", birth_year="1980"):
        sel = self.selenium
        sel.select("css=#id_birth_month", birth_month)
        sel.type("css=#id_birth_day", birth_day)
        sel.type("css=#id_birth_year", birth_year)
        time.sleep(4)
