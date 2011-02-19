from djangosanetesting.cases import SeleniumTestCase
import time 
from test_factory import Factory

def common_creating_and_editing_a_new_person(self):
    sel = self.selenium
    sel.open("/people/search")
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
    sel.click("id_first_name")
    time.sleep(2)
    sel.click("css=.start_edit_btn")
    time.sleep(1)
    try: self.assertEqual("John", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Smith", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("555-123-4567", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("john@smithfamily.com", sel.get_text("//span[@id='container_id_email']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("123 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Apt 27", sel.get_text("//span[@id='container_id_line_2']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Wilsonville", sel.get_text("//span[@id='container_id_city']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("KY", sel.get_text("//span[@id='container_id_state']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("12345", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    time.sleep(2)
    try: self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Saved", sel.get_text("css=.save_and_status_btn"))
    except AssertionError, e: self.verificationErrors.append(str(e))        
    
    sel.click("link=People")
    sel.wait_for_page_to_load("30000")
    sel.focus("css=#id_search_query")
    sel.type("css=#id_search_query", "john smith 555")
    sel.key_down("css=#id_search_query","5")
    sel.key_up("css=#id_search_query","5")
    time.sleep(2)
    self.assertEqual("John Smith", sel.get_text("css=search_results .result_row .name a"))
    sel.click("css=search_results .result_row .name a")
    sel.wait_for_page_to_load("30000")
    try: self.assertEqual("John", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Smith", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("555-123-4567", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("john@smithfamily.com", sel.get_text("link=john@smithfamily.com"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("123 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Apt 27", sel.get_text("//span[@id='container_id_line_2']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Wilsonville", sel.get_text("//span[@id='container_id_city']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("KY", sel.get_text("//span[@id='container_id_state']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("12345", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    sel.click("css=.start_edit_btn")
    time.sleep(1)

    sel.type("id_first_name", "Jon")
    sel.type("id_last_name", "Smithe")
    sel.type("id_phone_number", "555-765-4321")
    sel.type("id_email", "jon@smithefamily.com")
    sel.type("id_line_1", "1234 Main St")
    sel.type("id_line_2", "")
    sel.type("id_city", "Williamsburg")
    sel.type("id_state", "TN")
    sel.type("id_postal_code", "54321")
    sel.type("id_first_name")
    time.sleep(2)
    sel.click("css=.edit_done_btn")
    time.sleep(1)
    sel.click("link=People")
    sel.wait_for_page_to_load("30000")
    sel.focus("css=#id_search_query")
    sel.type("css=#id_search_query", "jon smithe 555")
    sel.key_down("css=#id_search_query","5")
    sel.key_up("css=#id_search_query","5")
    time.sleep(2)
    sel.click("//div[@id='page']/div[2]/table/tbody/tr[2]/td[1]/a/b[2]")
    sel.wait_for_page_to_load("30000")
    self.assertEqual("Jon", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
    try: self.assertEqual("Smithe", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("555-765-4321", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("jon@smithefamily.com", sel.get_text("link=jon@smithefamily.com"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("1234 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("Williamsburg", sel.get_text("//span[@id='container_id_city']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("TN", sel.get_text("//span[@id='container_id_state']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    try: self.assertEqual("54321", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    return self

class TestAgainstNoData(SeleniumTestCase):
    def setUp(self):
        self.verificationErrors = []
    
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)

    def test_creating_and_editing_a_new_person(self):
        sel = self.selenium
        sel.open("/people/search")
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
        time.sleep(5)        
        try: self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Saved", sel.get_text("css=.save_and_status_btn"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=.edit_done_btn")
        time.sleep(1)        
        try: self.assertEqual("John", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Smith", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("555-123-4567", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("john@smithfamily.com", sel.get_text("//span[@id='container_id_email']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("123 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Apt 27", sel.get_text("//span[@id='container_id_line_2']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Wilsonville", sel.get_text("//span[@id='container_id_city']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("KY", sel.get_text("//span[@id='container_id_state']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("12345", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "john smith 555")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")
        time.sleep(3)
        self.assertEqual("John Smith", sel.get_text("css=search_results .result_row .name a"))
        sel.click("css=search_results .result_row .name a")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("John", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Smith", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("555-123-4567", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("john@smithfamily.com", sel.get_text("link=john@smithfamily.com"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("123 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Apt 27", sel.get_text("//span[@id='container_id_line_2']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Wilsonville", sel.get_text("//span[@id='container_id_city']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("KY", sel.get_text("//span[@id='container_id_state']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("12345", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.type("id_first_name", "Jon")
        sel.type("id_last_name", "Smithe")
        sel.type("id_phone_number", "555-765-4321")
        sel.type("id_email", "jon@smithefamily.com")
        sel.type("id_line_1", "1234 Main St")
        sel.type("id_line_2", "")
        sel.type("id_city", "Williamsburg")
        sel.type("id_state", "TN")
        sel.type("id_postal_code", "54321")
        sel.click("id_first_name",)
        time.sleep(4)
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "jon smithe 555")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")
        time.sleep(2)
        sel.click("css=search_results .result_row .name a")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Jon", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
        try: self.assertEqual("Smithe", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("555-765-4321", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("jon@smithefamily.com", sel.get_text("link=jon@smithefamily.com"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1234 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Williamsburg", sel.get_text("//span[@id='container_id_city']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("TN", sel.get_text("//span[@id='container_id_state']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("54321", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))

    def test_search_page_loads(self):
        sel = self.selenium
        sel.open("/people/search")
        sel.wait_for_page_to_load("30000")

class TestAgainstGeneratedData(SeleniumTestCase):
    # selenium_fixtures = ["200_test_people.json"]
    
    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    
    def tearDown(self,*args, **kwargs):
        for p in self.people:
            p.delete()
        self.assertEqual([], self.verificationErrors)


    def test_creating_and_editing_a_new_person_with_generated(self):
        sel = self.selenium
        sel.open("/people/search")
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
        sel.key_down("css=#id_postal_code","5")
        sel.key_up("css=#id_postal_code","5")
        time.sleep(4)
        self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        self.assertEqual("Saved", sel.get_text("css=.save_and_status_btn"))        
        sel.click("css=.edit_done_btn")
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


        
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "john smith 555")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")
        time.sleep(3)
        self.assertEqual("John Smith", sel.get_text("css=search_results .result_row .name a"))
        sel.click("css=search_results .result_row .name a")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("John", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
        self.assertEqual("Smith", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
        self.assertEqual("555-123-4567", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
        self.assertEqual("john@smithfamily.com", sel.get_text("link=john@smithfamily.com"))
        self.assertEqual("123 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        self.assertEqual("Apt 27", sel.get_text("//span[@id='container_id_line_2']/span[1]"))
        self.assertEqual("Wilsonville", sel.get_text("//span[@id='container_id_city']/span[1]"))
        self.assertEqual("KY", sel.get_text("//span[@id='container_id_state']/span[1]"))
        self.assertEqual("12345", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.type("id_first_name", "Jon")
        sel.type("id_last_name", "Smithe")
        sel.type("id_phone_number", "555-765-4321")
        sel.type("id_email", "jon@smithefamily.com")
        sel.type("id_line_1", "1234 Main St")
        sel.type("id_line_2", "")
        sel.type("id_city", "Williamsburg")
        sel.type("id_state", "TN")
        sel.type("id_postal_code", "54321")
        sel.key_down("css=#id_postal_code","1")
        sel.key_up("css=#id_postal_code","1")
        time.sleep(4)
        self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        self.assertEqual("Saved", sel.get_text("css=.save_and_status_btn"))        
        sel.click("css=.edit_done_btn")
        time.sleep(1)
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "jon smithe 555")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")
        time.sleep(2)
        sel.click("css=search_results .result_row .name a")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Jon", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
        try: self.assertEqual("Smithe", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("555-765-4321", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("jon@smithefamily.com", sel.get_text("link=jon@smithefamily.com"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("1234 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Williamsburg", sel.get_text("//span[@id='container_id_city']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("TN", sel.get_text("//span[@id='container_id_state']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("54321", sel.get_text("css=#container_id_postal_code .view_field"))
        except AssertionError, e: self.verificationErrors.append(str(e))

    
    def test_search_page_loads(self):
        sel = self.selenium
        sel.open("/people/search")
        sel.wait_for_page_to_load("30000")

    # def test_search_page_updates(self):
    #     sel = self.selenium
    #     sel.open("/people/search")
    #     sel.wait_for_page_to_load("30000")
    #     sel.key_press("css=#id_search_query","a")
    #     time.sleep(1)

    def test_editing_and_searching_a_record(self):
        sel = self.selenium
        sel.open("/people/search")
        sel.type("css=#id_search_query", "a")
        sel.click("css=search_results .result_row .name a")
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(1)

        sel.type("id_first_name", "Jennifer")
        sel.type("id_last_name", "Williamsburg")
        sel.type("id_phone_number", "520-845-6732")
        sel.type("id_email", "jdawg@gmail.com")
        sel.type("id_line_1", "12445 SE Stark St.")
        sel.type("id_line_2", "")
        sel.type("id_city", "Kalamazoo")
        sel.type("id_state", "MI")
        sel.type("id_postal_code", "12346")
        sel.click("css=.save_and_status_btn")
        time.sleep(4)
        try: self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Saved", sel.get_text("css=.save_and_status_btn"))
        except AssertionError, e: self.verificationErrors.append(str(e))        
        sel.click("css=main_nav a:contains('People')")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "jennifer williamsburg 520")
        sel.key_down("css=#id_search_query","0")
        sel.key_up("css=#id_search_query","0")
        try: self.assertEqual("Jennifer", sel.get_text("css=search_results .result_row .name a b"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("520", sel.get_text("css=search_results .result_row .phone_number b"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("520-845-6732", sel.get_text("css=search_results .result_row .phone_number"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("css=search_results .result_row .name a")
        sel.wait_for_page_to_load("30000")
        try: self.assertEqual("Jennifer", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Williamsburg", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("520-845-6732", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("jdawg@gmail.com", sel.get_text("link=jdawg@gmail.com"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("12445 SE Stark St.", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("Kalamazoo", sel.get_text("//span[@id='container_id_city']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("MI", sel.get_text("//span[@id='container_id_state']/span[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("12346", sel.get_text("css=#container_id_postal_code .view_field"))
        except AssertionError, e: self.verificationErrors.append(str(e))

    def test_editing_an_email_or_phone_number_changes_the_search_result(self):
        sel = self.selenium
        sel.open("/people/search")
        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.type("id_email", "newemail@test.com")
        time.sleep(2)
        sel.click("css=.edit_done_btn")
        sel.click("link=People")
        
        try: self.assertEqual("newemail@test.com", sel.get_text("css=search_results .result_row:nth(0) .email a"))
        except AssertionError, e: self.verificationErrors.append(str(e))

        sel = self.selenium
        sel.open("/people/search")
        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.type("id_phone_number", "555 123-4567")
        time.sleep(2)
        sel.click("css=.edit_done_btn")
        sel.click("link=People")

        try: self.assertEqual("555 123-4567", sel.get_text("css=search_results .result_row:nth(0) .phone_number"))
        except AssertionError, e: self.verificationErrors.append(str(e))        

    def test_creating_and_editing_an_organization(self):
        sel = self.selenium
        sel.open("/people/")
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
        time.sleep(3)
        sel.click("link=Back to All People and Organizations")
        sel.wait_for_page_to_load("30000")

        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "Test Organ")
        sel.key_down("css=#id_search_query","n")
        sel.key_up("css=#id_search_query","n")
        
        self.assertEqual("555 123-4567", sel.get_text("css=search_results .result_row:nth(0) .phone_number"))
        self.assertEqual("Test", sel.get_text("//div[@id='page']/search_results/fragment/table/tbody/tr[2]/td[1]/a/span/b[1]"))
        sel.click("//div[@id='page']/search_results/fragment/table/tbody/tr[2]/td[1]/a/span")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Test Organization", sel.get_text("//span[@id='container_id_name']/span[1]"))
        self.assertEqual("example.com", sel.get_text("link=example.com"))
        self.assertEqual("@testorg", sel.get_text("link=@testorg"))
        self.assertEqual("123 1st St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        sel.click("link=Edit Organization")
        sel.click("id_name")
        sel.type("id_name", "Test Org")
        sel.type("id_primary_phone_number", "555 123-4568")
        sel.type("id_website", "example.org")
        sel.type("id_twitter_username", "testorgz")
        sel.type("id_line_1", "128 1st St")
        sel.type("id_line_2", "#120")
        sel.type("id_city", "Williamsborough")
        sel.type("id_state", "IN")
        sel.type("id_postal_code", "45321")
        sel.click("link=Save Now")
        time.sleep(3)
        sel.refresh()
        time.sleep(4)
        self.assertEqual("Test Org", sel.get_text("//span[@id='container_id_name']/span[1]"))
        self.assertEqual("555 123-4568", sel.get_text("//span[@id='container_id_primary_phone_number']/span[1]"))        
        self.assertEqual("example.org", sel.get_text("link=example.org"))
        self.assertEqual("@testorgz", sel.get_text("link=@testorgz"))
        self.assertEqual("128 1st St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        self.assertEqual("#120", sel.get_text("//span[@id='container_id_line_2']/span[1]"))
        self.assertEqual("Williamsborough", sel.get_text("//span[@id='container_id_city']/span[1]"))
        self.assertEqual("IN", sel.get_text("//span[@id='container_id_state']/span[1]"))
        self.assertEqual("45321", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))
        
