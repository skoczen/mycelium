import time 
from test_factory import Factory

from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from people.tests.selenium_abstractions import PeopleTestAbstractions

class TestAgainstNoData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, AccountTestAbstractions):
    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_with_no_data()
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
        

    def test_creating_and_editing_an_organization(self):
        sel = self.selenium
        self.create_new_organization_and_return_to_search()
        
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "Test Organ")
        sel.key_down("css=#id_search_query","n")
        sel.key_up("css=#id_search_query","n")
        time.sleep(2)

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
        sel.click("link=Back to All People and Organizations")
        sel.wait_for_page_to_load("30000")

        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "Test Org")
        sel.key_down("css=#id_search_query","n")
        sel.key_up("css=#id_search_query","n")
        time.sleep(2)

        self.assertEqual("555 123-4568", sel.get_text("css=search_results .result_row:nth(0) .phone_number"))        

    def test_adding_people_to_an_organization(self):
        sel = self.selenium
        self.create_new_organization()
        time.sleep(2)
        sel.click("css=tabbed_box tab_title")
        time.sleep(0.5)
        sel.click("id_search_new_person")
        sel.type("id_search_new_person", "Joe Smith")
        sel.click("link=Add a New Person")
        sel.click("css=#new_person form input[id$=role]")
        sel.type("css=#new_person form input[id$=role]", "Chief Tester")
        sel.type("css=#new_person form input[id$=email]", "joesmith@myneworg.org")
        sel.type("css=#new_person form input[id$=phone_number]", "503-247.8451")
        sel.click("//div[@id='new_person']/form/form_actions/input")
        time.sleep(2)
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Joe Smith", sel.get_text("link=Joe Smith"))
        self.assertEqual("Chief Tester", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("503-247.8451", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("joesmith@myneworg.org", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=email] .view_field"))        
        sel.click("css=tabbed_box tab_title")
        sel.click("css=tabbed_box box_close a")
        sel.click("link=Back to All People and Organizations")
        sel.wait_for_page_to_load("30000")
        sel.click("link=New Person")
        sel.wait_for_page_to_load("30000")
        sel.type("id_first_name", "Bill")
        sel.type("id_last_name", "Williams")
        sel.click("link=Save Now")
        time.sleep(2)
        sel.click("link=Done")
        sel.click("link=Back to All People")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "Test Organization 555123")
        sel.key_down("css=#id_search_query","g")
        sel.key_up("css=#id_search_query","g")
        time.sleep(1)
        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        sel.click("css=tabbed_box tab_title")
        sel.type("id_search_new_person", "Bill Will")
        sel.click("link=Add this Person")
        time.sleep(2)
        sel.type("id_EMPLOYEE-role", "Chief Already Here Person")
        sel.type("id_EMPLOYEE-email", "bill@myneworg.org")
        sel.type("id_EMPLOYEE-phone_number", "555-123-4567x264")
        sel.click("//div[@id='add_existing_person']/form/form_actions")
        sel.click("//input[@value='Add this Person']")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Bill Williams", sel.get_text("link=Bill Williams"))
        self.assertEqual("Chief Already Here Person", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("555-123-4567x264", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("bill@myneworg.org", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=email] .view_field"))        


    def test_adding_people_to_an_org_shows_on_their_people_page(self):
        sel = self.selenium
        self.create_new_organization()
        time.sleep(2)
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
        sel.click("link=Back to All People and Organizations")
        sel.wait_for_page_to_load("30000")

        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "joyellen smith")
        sel.key_down("css=#id_search_query","h")
        sel.key_up("css=#id_search_query","h")
        time.sleep(2)
        sel.click("css=search_results .result_row .name a")
        sel.wait_for_page_to_load("30000")

        self.assertEqual("Test Organization", sel.get_text("css=tabbed_box[name=job]:nth(0) tab_title text"))
        self.assertEqual("Chief Tester", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("503-247.8451", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("joesmith@myneworg.org", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=email] .view_field"))
        sel.click("link=Edit Person")
        sel.type("id_ROLE-0-role", "Chief Pooh-bah Tester")
        sel.type("id_ROLE-0-phone_number", "503 247-8451")
        sel.type("id_ROLE-0-email", "joysmith@myneworg.org")
        time.sleep(2)
        sel.click("link=Done")
        time.sleep(1)
        self.assertEqual("Chief Pooh-bah Tester", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("503 247-8451", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("joysmith@myneworg.org", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=email] .view_field"))

        sel.click("css=tabbed_box[name=job]:nth(0) tab_title")
        sel.wait_for_page_to_load("30000")


        sel.wait_for_page_to_load("30000")
        self.assertEqual("Joyellen Smith", sel.get_text("css=employee:nth(0) .name"))
        self.assertEqual("Chief Pooh-bah Tester", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("503 247-8451", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("joysmith@myneworg.org", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=email] .view_field"))

    def test_users_should_be_able_to_edit_work_info_via_the_org_page_and_have_the_changes_reflected_on_the_people_page(self):
        sel = self.selenium
        self.open("/people/")
        self.create_new_organization()
        time.sleep(2)
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
        sel.click("link=Back to All People and Organizations")
        sel.wait_for_page_to_load("30000")

        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "joyellen smith")
        sel.key_down("css=#id_search_query","h")
        sel.key_up("css=#id_search_query","h")
        time.sleep(2)
        sel.click("css=search_results .result_row .name a")
        sel.wait_for_page_to_load("30000")

        self.assertEqual("Chief Tester", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("503-247.8451", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("joesmith@myneworg.org", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=email] .view_field"))

        sel.click("link=Back to All People")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "Test Org 555123")
        sel.key_down("css=#id_search_query","g")
        sel.key_up("css=#id_search_query","g")
        time.sleep(1)
        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        sel.click("css=employee:nth(0) .start_edit_btn")
        time.sleep(1)

        sel.type("css=#id_ROLE-0-role","Chief Tester ++")
        sel.type("css=#id_ROLE-0-phone_number","555 123-4567x123")
        sel.type("css=#id_ROLE-0-email","joy55@example.com")
        time.sleep(1)
        sel.click("css=employee:nth(0) .edit_done_btn")
        time.sleep(1)

        sel.click("link=Back to All People and Organizations")
        sel.wait_for_page_to_load("30000")

        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "joyellen smith")
        sel.key_down("css=#id_search_query","h")
        sel.key_up("css=#id_search_query","h")
        time.sleep(2)
        sel.click("css=search_results .result_row .name a")
        sel.wait_for_page_to_load("30000")

        self.assertEqual("Chief Tester ++", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("555 123-4567x123", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("joy55@example.com", sel.get_text("css=tabbed_box[name=job]:nth(0) box_content .generic_editable_field[id$=email] .view_field"))



    def test_users_should_be_able_to_dissassociate_a_person_from_an_organization_via_the_organization_page(self):
        sel = self.selenium
        self.create_new_organization()
        time.sleep(2)
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

        sel.click("id_search_new_person")
        sel.type("id_search_new_person", "William Blinkerton")
        sel.click("link=Add a New Person")
        sel.click("css=#new_person form input[id$=role]")
        sel.type("css=#new_person form input[id$=role]", "Head Honcho")
        sel.type("css=#new_person form input[id$=email]", "will_blinkerton@myneworg.org")
        sel.type("css=#new_person form input[id$=phone_number]", "444-123-7890")
        sel.click("//div[@id='new_person']/form/form_actions/input")
        time.sleep(2)
        sel.wait_for_page_to_load("30000")
        self.assertEqual("William Blinkerton", sel.get_text("link=William Blinkerton"))
        self.assertEqual("Head Honcho", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("444-123-7890", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("will_blinkerton@myneworg.org", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=email] .view_field"))        

        self.assertEqual("Joyellen Smith", sel.get_text("link=Joyellen Smith"))
        self.assertEqual("Chief Tester", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("503-247.8451", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("joesmith@myneworg.org", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=email] .view_field"))

        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual("William Blinkerton", sel.get_text("link=William Blinkerton"))
        self.assertEqual("Head Honcho", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("444-123-7890", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("will_blinkerton@myneworg.org", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=email] .view_field"))        
        sel.click("css=employee:nth(1) .start_edit_btn")
        time.sleep(2)

        sel = self.selenium
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=employee:nth(1) .delete_contact_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to remove William Blinkerton from Test Organization?\n\nThis will not remove William Blinkerton from the database, only from this role at Test Organization.")
        self.assertEqual("William Blinkerton", sel.get_text("link=William Blinkerton"))
        self.assertEqual("Head Honcho", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("444-123-7890", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("will_blinkerton@myneworg.org", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=email] .view_field"))        

        self.assertEqual("William Blinkerton", sel.get_text("link=William Blinkerton"))
        self.assertEqual("Head Honcho", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("444-123-7890", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("will_blinkerton@myneworg.org", sel.get_text("css=employee:nth(1) .generic_editable_field[id$=email] .view_field"))        

        sel.click("css=employee:nth(1) .delete_contact_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to remove William Blinkerton from Test Organization?\n\nThis will not remove William Blinkerton from the database, only from this role at Test Organization.")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Joyellen Smith", sel.get_text("link=Joyellen Smith"))
        self.assertEqual("Chief Tester", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=role] .view_field"))
        self.assertEqual("503-247.8451", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=phone_number] .view_field"))
        self.assertEqual("joesmith@myneworg.org", sel.get_text("css=employee:nth(0) .generic_editable_field[id$=email] .view_field"))        

        assert not sel.is_text_present("William Blinkerton")

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


    def test_people_with_no_home_contact_but_business_info_should_have_their_biz_contact_info_listed_in_search(self):
        sel = self.selenium
        self.open("/people/")
        self.create_new_organization()
        time.sleep(2)
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
        sel.click("link=Back to All People and Organizations")
        sel.wait_for_page_to_load("30000")

        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "joyellen smith")
        sel.key_down("css=#id_search_query","h")
        sel.key_up("css=#id_search_query","h")
        time.sleep(1)
        self.assertEqual("Joyellen Smith", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        self.assertEqual("503-247.8451", sel.get_text("css=search_results .result_row:nth(0) .phone_number"))
        self.assertEqual("joesmith@myneworg.org", sel.get_text("css=search_results .result_row:nth(0) .email"))                

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
        sel.close()
        sel.select_window("one")        
        sel.refresh()
        time.sleep(4)

        self.assertEqual("Jon", sel.get_text("//span[@id='container_id_first_name']/span[1]"))
        self.assertEqual("Smithe", sel.get_text("//span[@id='container_id_last_name']/span[1]"))

        self.assertEqual("555-765-4321", sel.get_text("//span[@id='container_id_phone_number']/span[1]"))

        self.assertEqual("jon@smithefamily.com", sel.get_text("link=jon@smithefamily.com"))

        self.assertEqual("1234 Main St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))

        self.assertEqual("Williamsburg", sel.get_text("//span[@id='container_id_city']/span[1]"))

        self.assertEqual("TN", sel.get_text("//span[@id='container_id_state']/span[1]"))

        self.assertEqual("54321", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))


    def test_that_closing_an_organization_page_makes_sure_the_changes_are_saved(self):
        sel = self.selenium

        self.open_window("/people/", "one")
        sel.select_window("one")
        self.create_new_organization_and_return_to_search()

        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "Test Organ")
        sel.key_down("css=#id_search_query","n")
        sel.key_up("css=#id_search_query","n")
        time.sleep(2)

        self.assertEqual("555 123-4567", sel.get_text("css=search_results .result_row:nth(0) .phone_number"))
        self.assertEqual("Test", sel.get_text("//div[@id='page']/search_results/fragment/table/tbody/tr[2]/td[1]/a/span/b[1]"))
        sel.click("//div[@id='page']/search_results/fragment/table/tbody/tr[2]/td[1]/a/span")

        self.open_window("/people/", "two")
        sel.select_window("two")
        time.sleep(2)

        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "Test Organ")
        sel.key_down("css=#id_search_query","n")
        sel.key_up("css=#id_search_query","n")
        time.sleep(2)

        self.assertEqual("555 123-4567", sel.get_text("css=search_results .result_row:nth(0) .phone_number"))
        self.assertEqual("Test", sel.get_text("//div[@id='page']/search_results/fragment/table/tbody/tr[2]/td[1]/a/span/b[1]"))
        sel.click("//div[@id='page']/search_results/fragment/table/tbody/tr[2]/td[1]/a/span")

        sel.wait_for_page_to_load("30000")
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
        sel.close()

        sel.select_window("one")
        sel.refresh()
        sel.wait_for_page_to_load("30000")

        self.assertEqual("Test Org", sel.get_text("//span[@id='container_id_name']/span[1]"))
        self.assertEqual("555 123-4568", sel.get_text("//span[@id='container_id_primary_phone_number']/span[1]"))        
        self.assertEqual("example.org", sel.get_text("link=example.org"))
        self.assertEqual("@testorgz", sel.get_text("link=@testorgz"))
        self.assertEqual("128 1st St", sel.get_text("//span[@id='container_id_line_1']/span[1]"))
        self.assertEqual("#120", sel.get_text("//span[@id='container_id_line_2']/span[1]"))
        self.assertEqual("Williamsborough", sel.get_text("//span[@id='container_id_city']/span[1]"))
        self.assertEqual("IN", sel.get_text("//span[@id='container_id_state']/span[1]"))
        self.assertEqual("45321", sel.get_text("//span[@id='container_id_postal_code']/span[1]"))

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

        self.assertEqual("No Name", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "No Name")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")
        time.sleep(3)
        self.assertEqual("No Name", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.person_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Unnamed Person from the database? \n\nDeleting will remove this person, and all their data (contact info, job info, etc).  It cannot be undone.\n\nPress OK to delete Unnamed Person.\nPress Cancel to leave things unchanged.")
        sel.click("css=.person_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Unnamed Person from the database? \n\nDeleting will remove this person, and all their data (contact info, job info, etc).  It cannot be undone.\n\nPress OK to delete Unnamed Person.\nPress Cancel to leave things unchanged.")
        sel.wait_for_page_to_load("30000")
        
        assert not sel.is_text_present("No Name")
    
    
    def test_creating_and_deleting_a_blank_organization(self):
        sel = self.selenium
        self.open("/people/")
        sel.click("link=New Organization")
        sel.wait_for_page_to_load("30000")
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")

        self.assertEqual("No Name", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "No Name")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")
        time.sleep(2)
        self.assertEqual("No Name", sel.get_text("css=search_results .result_row:nth(0) .name a"))

        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        time.sleep(3)
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.org_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Unnamed Organization from the database? \n\nDeleting will remove this organization and all their data (contact info, employees, etc).  The people associated with this organization will not be removed.\n\nThis action cannot be undone.\n\nPress OK to delete Unnamed Organization.\nPress Cancel to leave things unchanged.")
        sel.click("css=.org_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Unnamed Organization from the database? \n\nDeleting will remove this organization and all their data (contact info, employees, etc).  The people associated with this organization will not be removed.\n\nThis action cannot be undone.\n\nPress OK to delete Unnamed Organization.\nPress Cancel to leave things unchanged.")

        sel.wait_for_page_to_load("30000")
        assert not sel.is_text_present("No Name")

    
    def test_creating_and_deleting_a_new_organization(self):
        sel = self.selenium
        self.create_new_organization_and_return_to_search()

        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "Test Organ")

        time.sleep(3)
        self.assertEqual("Test Organization", sel.get_text("css=search_results .result_row:nth(0) .name a"))

        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.org_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Test Organization from the database? \n\nDeleting will remove this organization and all their data (contact info, employees, etc).  The people associated with this organization will not be removed.\n\nThis action cannot be undone.\n\nPress OK to delete Test Organization.\nPress Cancel to leave things unchanged.")
        sel.click("css=.org_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Test Organization from the database? \n\nDeleting will remove this organization and all their data (contact info, employees, etc).  The people associated with this organization will not be removed.\n\nThis action cannot be undone.\n\nPress OK to delete Test Organization.\nPress Cancel to leave things unchanged.")
        
        sel.wait_for_page_to_load("30000")
        assert not sel.is_text_present("Test Organization")


    def test_that_search_ordering_for_people_and_orgs_is_mixed(self):
        sel = self.selenium
        self.open("/people/")
        sel.click("link=New Organization")
        sel.wait_for_page_to_load("30000")
        sel.type("id_name", "Foo Test Organization")
        sel.click("link=Back to All People and Organizations")
        sel.wait_for_page_to_load("30000")


        sel.click("link=New Person")
        sel.wait_for_page_to_load("30000")
        sel.type("id_first_name", "John")
        sel.type("id_last_name", "Smith")
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")

        sel.click("link=New Person")
        sel.wait_for_page_to_load("30000")
        sel.type("id_first_name", "Alfred")
        sel.type("id_last_name", "Williams")
        # wait for celery to catch up.
        time.sleep(5)
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")

        self.assertEqual("Alfred Williams", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        self.assertEqual("Foo Test Organization", sel.get_text("css=search_results .result_row:nth(1) .name a"))
        self.assertEqual("John Smith", sel.get_text("css=search_results .result_row:nth(2) .name a"))
        sel.click("css=search_results .result_row:nth(1) .name a")
        sel.wait_for_page_to_load("30000")

        sel.click("link=Edit Organization")
        sel.click("id_name")
        sel.type("id_name", "Test Organization")
        # wait for celery to catch up.
        time.sleep(5)
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        self.assertEqual("Alfred Williams", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        self.assertEqual("John Smith", sel.get_text("css=search_results .result_row:nth(1) .name a"))
        self.assertEqual("Test Organization", sel.get_text("css=search_results .result_row:nth(2) .name a"))

    def test_that_the_last_selected_tab_stays_open_after_refresh_in_people(self):
        sel = self.selenium
        self.create_john_smith()
        time.sleep(4)
        assert not sel.is_text_present("Volunteer Shifts")
        sel.click("css=.detail_tab[href=#volunteer]")
        time.sleep(2)
        assert sel.is_text_present("Volunteer Shifts")
        self.js_refresh()
        assert sel.is_text_present("Volunteer Shifts")


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
        sel.click("css=main_nav a:contains('People')")
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
        assert not sel.is_text_present("No Name")
        sel.click("link=New Person")
        sel.wait_for_page_to_load("30000")
        # celery catch-up
        time.sleep(5)
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")

        self.assertEqual("No Name", sel.get_text("css=search_results .result_row:nth(0) .name a"))


    def test_that_blank_organizations_show_at_the_top_of_the_search(self):
        sel = self.selenium
        self.open("/people/")
        assert not sel.is_text_present("No Name")
        sel.click("link=New Organization")
        sel.wait_for_page_to_load("30000")
        # celery catch-up
        time.sleep(5)
        sel.click("link=Back to All People and Organizations")
        sel.wait_for_page_to_load("30000")

        self.assertEqual("No Name", sel.get_text("css=search_results .result_row:nth(0) .name a"))

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


