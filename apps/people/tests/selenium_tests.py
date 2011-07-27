import time 
from test_factory import Factory

from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from people.tests.selenium_abstractions import PeopleTestAbstractions
from django.core.cache import cache

class TestAgainstNoData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_with_no_data()
        cache.clear()
        self.verificationErrors = []

    # def tearDown(self):
    #     self.account.delete()

    def test_creating_and_editing_a_new_person(self):
        sel = self.selenium
        self.create_john_smith()
        
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "john smith 555")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")

        time.sleep(3)
        self.assertEqual("John Smith", sel.get_text("css=search_results .result_row:nth(0) .name a"))

        sel.click("css=search_results .result_row:nth(0) .name a")
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
        self.assertEqual("Smithe", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
        self.assertEqual("555-765-4321", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
        self.assertEqual("jon@smithefamily.com", sel.get_text("link=jon@smithefamily.com"))
        self.assertEqual("1234 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        self.assertEqual("Williamsburg", sel.get_text("//span[@id='container_id_city']/span[1]"))
        self.assertEqual("TN", sel.get_text("//span[@id='container_id_state']/span[1]"))
        self.assertEqual("54321", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))

    def test_search_page_loads(self):
        sel = self.selenium
        self.open("/people/search")
        sel.wait_for_page_to_load("30000")
        

    def test_that_the_last_saved_text_updates_properly(self):
        sel = self.selenium
        self.create_john_smith()
        time.sleep(4)
        self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        self.assertEqual("Saved", sel.get_text("css=.save_and_status_btn"))    
        time.sleep(60)
        sel.refresh()
        sel.wait_for_page_to_load("30000")

        self.assertEqual("Last changed 1 minute ago.", sel.get_text("css=.last_save_time"))
        self.assertEqual("Saved", sel.get_text("css=.save_and_status_btn"))

    def test_that_closing_a_person_page_makes_sure_the_changes_are_saved(self):
        sel = self.selenium

        self.open_window("/people/search", "one")
        sel.select_window("one")        

        self.create_john_smith_and_return_to_search()

        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "john smith 555")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")

        time.sleep(3)
        self.assertEqual("John Smith", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")

        self.open_window("/people/search", "two")
        sel.select_window("two")
        time.sleep(4)
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "john smith 555")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")

        time.sleep(3)
        self.assertEqual("John Smith", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")

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
        time.sleep(0.5)
        sel.close()
        sel.select_window("one")        
        time.sleep(4)
        sel.refresh()
        

        self.assertEqual("Jon", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
        self.assertEqual("Smithe", sel.get_text("//span[@id='container_id_last_name']/span[1]"))
        self.assertEqual("555-765-4321", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))
        self.assertEqual("jon@smithefamily.com", sel.get_text("link=jon@smithefamily.com"))
        self.assertEqual("1234 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        self.assertEqual("Williamsburg", sel.get_text("//span[@id='container_id_city']/span[1]"))
        self.assertEqual("TN", sel.get_text("//span[@id='container_id_state']/span[1]"))
        self.assertEqual("54321", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))
        # TODO: This always fails on firefox.

    def test_creating_and_deleting_a_new_person(self):
        sel = self.selenium

        self.create_john_smith_and_return_to_search()
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "john smith 555")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")

        time.sleep(3)
        self.assertEqual("John Smith", sel.get_text("css=search_results .result_row:nth(0) .name a"))

        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.person_delete_btn")
        self.assertEqual(sel.get_confirmation(),"""Are you sure you want to completely delete John Smith from the database? \n\nDeleting will remove this person, and all their data (contact info, job info, etc).  It cannot be undone.\n\nPress OK to delete John Smith.\nPress Cancel to leave things unchanged.""")
        sel.click("css=.person_delete_btn")
        self.assertEqual(sel.get_confirmation(),"""Are you sure you want to completely delete John Smith from the database? \n\nDeleting will remove this person, and all their data (contact info, job info, etc).  It cannot be undone.\n\nPress OK to delete John Smith.\nPress Cancel to leave things unchanged.""")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "john smith 555")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")

        time.sleep(3)
        assert not sel.is_text_present("John Smith")
        
        

    def test_creating_and_deleting_a_blank_person(self):
        sel = self.selenium
        self.open("/people/search")
        sel.click("link=New Person")
        sel.wait_for_page_to_load("30000")
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")

        self.assertEqual("Unnamed Person", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "Unnamed Person")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")
        time.sleep(3)
        self.assertEqual("Unnamed Person", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.person_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Unnamed Person from the database? \n\nDeleting will remove this person, and all their data (contact info, job info, etc).  It cannot be undone.\n\nPress OK to delete Unnamed Person.\nPress Cancel to leave things unchanged.")
        sel.click("css=.person_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Unnamed Person from the database? \n\nDeleting will remove this person, and all their data (contact info, job info, etc).  It cannot be undone.\n\nPress OK to delete Unnamed Person.\nPress Cancel to leave things unchanged.")
        sel.wait_for_page_to_load("30000")
        
        assert not sel.is_text_present("Unnamed Person")
 



    def test_that_the_last_selected_tab_stays_open_after_refresh_in_people(self):
        sel = self.selenium
        self.create_john_smith()
        time.sleep(4)
        assert not sel.is_text_present("Add a Donation")
        sel.click("css=.detail_tab[href=#donor]")
        time.sleep(2)
        assert sel.is_text_present("Add a Donation")
        self.js_refresh()
        assert sel.is_text_present("Add a Donation")


    def test_editing_an_email_or_phone_number_changes_the_search_result(self):
        sel = self.selenium
        self.create_john_smith_and_return_to_search()
        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.type("css=#id_email", "newemail@test.com")
        time.sleep(4)
        sel.click("css=.edit_done_btn")
        sel.click("link=People")
        
        self.assertEqual("newemail@test.com", sel.get_text("css=search_results .result_row:nth(0) .email a"))


        sel = self.selenium
        self.open("/people/search")
        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.type("css=#id_phone_number", "555 123-4567")
        time.sleep(4)
        sel.click("css=.edit_done_btn")
        sel.click("link=People")

        self.assertEqual("555 123-4567", sel.get_text("css=search_results .result_row:nth(0) .phone_number"))
        

    def test_editing_a_birthday_saves(self):
        sel = self.selenium
        self.create_john_smith()
        self.save_a_birthday()
        sel.click("css=.edit_done_btn")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(0)"), "April")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(1)"), "9")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(2)"), "1980")

        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(0)"), "April")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(1)"), "9")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(2)"), "1980")


    def test_clearing_a_birthday_clears_it(self):
        sel = self.selenium
        self.test_editing_a_birthday_saves()
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.select("css=#id_birth_month", "Unknown")
        sel.type("css=#id_birth_day", "")
        sel.type("css=#id_birth_year", "")
        time.sleep(4)
        sel.click("css=.edit_done_btn")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(0)"), "Unknown")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(1)"), "")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(2)"), "")

        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(0)"), "Unknown")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(1)"), "")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(2)"), "")

  

    def test_entering_an_invalid_birthday_warns_and_saves_blank(self):
        sel = self.selenium
        self.test_editing_a_birthday_saves()
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        self.save_a_birthday(birth_day="29", birth_month="February", birth_year="1980")
        assert not sel.is_text_present("Hm.")
        self.save_a_birthday(birth_day="29", birth_month="February", birth_year="1981")
        assert sel.is_text_present("Hm.")
        time.sleep(4)
        sel.click("css=.edit_done_btn")
        time.sleep(1)
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(0)"), "February")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(1)"), "29")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(2)"), "1981")
        assert sel.is_text_present("Hm.")

        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(0)"), "Unknown")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(1)"), "")
        self.assertEqual(sel.get_text("css=.birthday .view_field:nth(2)"), "1981")
      




class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["200_test_people.json"]
    
    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
        self.people = [Factory.person(self.account) for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []

    # def tearDown(self):
    #     self.account.delete()
  

    def test_creating_and_editing_a_new_person_with_generated(self):
        sel = self.selenium
        self.create_john_smith_and_return_to_search()

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
        self.assertEqual("Smithe", sel.get_text("//span[@id='container_id_last_name']/span[1]"))

        self.assertEqual("555-765-4321", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))

        self.assertEqual("jon@smithefamily.com", sel.get_text("link=jon@smithefamily.com"))

        self.assertEqual("1234 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))

        self.assertEqual("Williamsburg", sel.get_text("//span[@id='container_id_city']/span[1]"))

        self.assertEqual("TN", sel.get_text("//span[@id='container_id_state']/span[1]"))

        self.assertEqual("54321", sel.get_text("css=#container_id_postal_code .view_field"))


    
    def test_search_page_loads(self):
        sel = self.selenium
        self.open("/people/search")
        sel.wait_for_page_to_load("30000")

    def test_editing_and_searching_a_record(self):
        sel = self.selenium
        self.open("/people/search")
        sel.click("link=New Person")
        sel.wait_for_page_to_load("30000")
        time.sleep(2)

        sel.type("css=#id_first_name", "Jennifer")
        sel.type("css=#id_last_name", "Williamsburg")
        sel.type("css=#id_phone_number", "520-845-6732")
        sel.type("css=#id_email", "jdawg@gmail.com")
        sel.type("css=#id_line_1", "12445 SE Stark St.")
        sel.type("css=#id_line_2", "")
        sel.type("css=#id_city", "Kalamazoo")
        sel.type("css=#id_state", "MI")
        sel.type("css=#id_postal_code", "12346")
        sel.click("link=Save Now")
        time.sleep(4)
        self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        self.assertEqual("Saved", sel.get_text("css=.save_and_status_btn"))
        sel.click("css=side_nav a:contains('People')")
        sel.wait_for_page_to_load("30000")
        time.sleep(1)
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "jennifer williamsburg 520")
        sel.key_down("css=#id_search_query","0")
        sel.key_up("css=#id_search_query","0")
        time.sleep(2)
        self.assertEqual("Jennifer", sel.get_text("css=search_results .result_row:nth(0) .name a b"))

        self.assertEqual("520", sel.get_text("css=search_results .result_row:nth(0) .phone_number b"))

        self.assertEqual("520-845-6732", sel.get_text("css=search_results .result_row:nth(0) .phone_number"))

        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Jennifer", sel.get_text("//span[@id='container_id_first_name']/span[1]"))

        self.assertEqual("Williamsburg", sel.get_text("//span[@id='container_id_last_name']/span[1]"))

        self.assertEqual("520-845-6732", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))

        self.assertEqual("jdawg@gmail.com", sel.get_text("link=jdawg@gmail.com"))

        self.assertEqual("12445 SE Stark St.", sel.get_text("//span[@id='container_id_line_1']/span[1]"))

        self.assertEqual("Kalamazoo", sel.get_text("//span[@id='container_id_city']/span[1]"))

        self.assertEqual("MI", sel.get_text("//span[@id='container_id_state']/span[1]"))

        self.assertEqual("12346", sel.get_text("css=#container_id_postal_code .view_field"))


    def test_that_blank_people_show_at_the_top_of_the_search(self):
        sel = self.selenium
        self.open("/people/")
        assert not sel.is_text_present("Unnamed Person")
        sel.click("link=New Person")
        sel.wait_for_page_to_load("30000")
        # celery catch-up
        time.sleep(5)
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")

        self.assertEqual("Unnamed Person", sel.get_text("css=search_results .result_row:nth(0) .name a"))


    def test_that_clicking_next_on_the_search_results_works(self):
        sel = self.selenium
        self.open("/people/")
        first_result = sel.get_text("css=search_results .result_row:nth(0) .name a")
        sel.click("css=.pagination .next")
        sel.wait_for_page_to_load("30000")

        assert first_result != sel.get_text("css=search_results .result_row:nth(0) .name a")


    def test_that_clicking_next_on_the_search_results_keeps_the_search(self):
        sel = self.selenium
        self.open("/people/")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "a")
        time.sleep(2)

        first_result = sel.get_text("css=search_results .result_row:nth(0) .name a")
        sel.click("css=.pagination .next")
        sel.wait_for_page_to_load("30000")

        assert first_result != sel.get_text("css=search_results .result_row:nth(0) .name a")
        sel.click("css=.pagination .prev")
        sel.wait_for_page_to_load("30000")
        assert first_result == sel.get_text("css=search_results .result_row:nth(0) .name a")

    def test_that_searching_for_a_b_highlights_sanely(self):
        sel = self.selenium
        self.open("/people/")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "a b")
        time.sleep(1)
        first_result = sel.get_text("css=search_results .result_row:nth(0)")
        assert first_result.find('<b>') == -1



