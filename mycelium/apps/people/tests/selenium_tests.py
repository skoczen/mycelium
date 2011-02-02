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
    sel.click("//div[@id='page_header']/span[1]/div[2]")
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
    try: self.assertEqual("Last saved a few seconds ago.", sel.get_text("//div[@id='page_header']/span[2]/span"))
    except AssertionError, e: self.verificationErrors.append(str(e))
    sel.click("link=People")
    sel.wait_for_page_to_load("30000")
    sel.focus("id_search_query")
    sel.type("id_search_query", "john smith 555")
    sel.key_down("id_search_query","5")
    sel.key_up("id_search_query","5")
    time.sleep(2)
    self.assertEqual("John Smith", sel.get_text("css=.search_results .result_row .name a"))
    sel.click("//div[@id='page']/div[2]/table/tbody/tr[2]/td[1]/a/b[2]")
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
    sel.click("//div[@id='page_header']/span[1]/div[2]")
    sel.type("id_first_name", "Jon")
    sel.type("id_last_name", "Smithe")
    sel.type("id_phone_number", "555-765-4321")
    sel.type("id_email", "jon@smithefamily.com")
    sel.type("id_line_1", "1234 Main St")
    sel.type("id_line_2", "")
    sel.type("id_city", "Williamsburg")
    sel.type("id_state", "TN")
    sel.type("id_postal_code", "54321")
    sel.click("//div[@id='page_header']/span[1]/div[2]")
    time.sleep(2)
    sel.click("link=People")
    sel.wait_for_page_to_load("30000")
    sel.focus("id_search_query")
    sel.type("id_search_query", "jon smithe 555")
    sel.key_down("id_search_query","5")
    sel.key_up("id_search_query","5")
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
        pass

    def tearDown(self):
        pass
            
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
        time.sleep(10)        
        sel.click("//div[@id='page_header']/span[1]/div[2]")
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
        try: self.assertEqual("12345", sel.get_text("css=#container_id_postal_code .view_field"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        time.sleep(10)
        try: self.assertEqual("Last saved a few seconds ago.", sel.get_text("//div[@id='page_header']/span[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("id_search_query")
        sel.type("id_search_query", "john smith 555")
        sel.key_down("id_search_query","5")
        sel.key_up("id_search_query","5")
        time.sleep(3)
        self.assertEqual("John Smith", sel.get_text("css=.search_results .result_row .name a"))
        sel.click("//div[@id='page']/div[2]/table/tbody/tr[2]/td[1]/a/b[2]")
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
        try: self.assertEqual("12345", sel.get_text("css=#container_id_postal_code .view_field"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='page_header']/span[1]/div[2]")
        sel.type("id_first_name", "Jon")
        sel.type("id_last_name", "Smithe")
        sel.type("id_phone_number", "555-765-4321")
        sel.type("id_email", "jon@smithefamily.com")
        sel.type("id_line_1", "1234 Main St")
        sel.type("id_line_2", "")
        sel.type("id_city", "Williamsburg")
        sel.type("id_state", "TN")
        sel.type("id_postal_code", "54321")
        time.sleep(4)
        sel.click("//div[@id='page_header']/span[1]/div[2]")
        time.sleep(1)
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("id_search_query")
        sel.type("id_search_query", "jon smithe 555")
        sel.key_down("id_search_query","5")
        sel.key_up("id_search_query","5")
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
        try: self.assertEqual("54321", sel.get_text("css=#container_id_postal_code .view_field"))
        except AssertionError, e: self.verificationErrors.append(str(e))

    def test_search_page_loads(self):
        sel = self.selenium
        sel.open("/people/search")
        sel.wait_for_page_to_load("30000")

class TestAgainstGeneratedData(SeleniumTestCase):
    # selenium_fixtures = ["200_test_people.json"]
    def setUp(self):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
    
    def tearDown(self):
        for p in self.people:
            p.delete()

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
        time.sleep(1)        
        sel.click("//div[@id='page_header']/span[1]/div[2]")
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
        try: self.assertEqual("12345", sel.get_text("css=#container_id_postal_code .view_field"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        time.sleep(4)
        try: self.assertEqual("Last saved a few seconds ago.", sel.get_text("//div[@id='page_header']/span[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("id_search_query")
        sel.type("id_search_query", "john smith 555")
        sel.key_down("id_search_query","5")
        sel.key_up("id_search_query","5")
        time.sleep(3)
        self.assertEqual("John Smith", sel.get_text("css=.search_results .result_row .name a"))
        sel.click("//div[@id='page']/div[2]/table/tbody/tr[2]/td[1]/a/b[2]")
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
        try: self.assertEqual("12345", sel.get_text("css=#container_id_postal_code .view_field"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='page_header']/span[1]/div[2]")
        sel.type("id_first_name", "Jon")
        sel.type("id_last_name", "Smithe")
        sel.type("id_phone_number", "555-765-4321")
        sel.type("id_email", "jon@smithefamily.com")
        sel.type("id_line_1", "1234 Main St")
        sel.type("id_line_2", "")
        sel.type("id_city", "Williamsburg")
        sel.type("id_state", "TN")
        sel.type("id_postal_code", "54321")
        time.sleep(10)
        sel.click("//div[@id='page_header']/span[1]/div[2]")
        time.sleep(1)
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("id_search_query")
        sel.type("id_search_query", "jon smithe 555")
        sel.key_down("id_search_query","5")
        sel.key_up("id_search_query","5")
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
    #     sel.key_press("id_search_query","a")
    #     time.sleep(1)

    def test_editing_and_searching_a_record(self):
        sel = self.selenium
        sel.open("/people/search")
        sel.type("id_search_query", "a")
        sel.click("//div[@id='page']/div[2]/table/tbody/tr[2]/td[1]/a")
        sel.wait_for_page_to_load("30000")
        sel.click("//div[@id='page_header']/span[1]/div[2]")
        sel.type("id_first_name", "Jennifer")
        sel.type("id_last_name", "Williamsburg")
        sel.type("id_phone_number", "520-845-6732")
        sel.type("id_email", "jdawg@gmail.com")
        sel.type("id_line_1", "12445 SE Stark St.")
        sel.type("id_line_2", "")
        sel.type("id_city", "Kalamazoo")
        sel.type("id_state", "MI")
        sel.type("id_postal_code", "12346")
        sel.click("//div[@id='page_header']/span[1]/div[2]")
        time.sleep(10)
        try: self.assertEqual("Last saved a few seconds ago.", sel.get_text("//div[@id='page_header']/span[2]/span"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("id_search_query")
        sel.type("id_search_query", "jennifer williamsburg 520")
        sel.key_down("id_search_query","0")
        sel.key_up("id_search_query","0")
        try: self.assertEqual("Jennifer", sel.get_text("//div[@id='page']/div[2]/table/tbody/tr[2]/td[1]/a/b[1]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("520", sel.get_text("//div[@id='page']/div[2]/table/tbody/tr[2]/td[2]/b"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        try: self.assertEqual("520-845-6732", sel.get_text("//div[@id='page']/div[2]/table/tbody/tr[2]/td[2]"))
        except AssertionError, e: self.verificationErrors.append(str(e))
        sel.click("//div[@id='page']/div[2]/table/tbody/tr[2]/td[1]/a/b[2]")
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