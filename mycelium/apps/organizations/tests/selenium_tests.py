import time 
from test_factory import Factory

from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from people.tests.selenium_abstractions import PeopleTestAbstractions
from organizations.tests.selenium_abstractions import OrganizationsTestAbstractions


class TestAgainstNoData(QiConservativeSeleniumTestCase, OrganizationsTestAbstractions, AccountTestAbstractions):
    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_with_no_data()
        self.verificationErrors = []

    # def tearDown(self):
    #     self.account.delete()

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
        sel.click("link=Organizations")
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
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")
        sel.click("link=New Person")
        sel.wait_for_page_to_load("30000")
        sel.type("id_first_name", "Bill")
        sel.type("id_last_name", "Williams")
        sel.click("link=Save Now")
        time.sleep(2)
        sel.click("link=Done")
        sel.click("link=Organizations")
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
        sel.click("link=People")
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
        self.get_to_organizations_search()
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
        sel.click("link=People")
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

        sel.click("link=People")
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

        sel.click("link=People")
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


    def test_people_with_no_home_contact_but_business_info_should_have_their_biz_contact_info_listed_in_search(self):
        sel = self.selenium
        self.get_to_organizations_search()
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
        sel.click("link=People")
        sel.wait_for_page_to_load("30000")

        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "joyellen smith")
        sel.key_down("css=#id_search_query","h")
        sel.key_up("css=#id_search_query","h")
        time.sleep(1)
        self.assertEqual("Joyellen Smith", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        self.assertEqual("503-247.8451", sel.get_text("css=search_results .result_row:nth(0) .phone_number"))
        self.assertEqual("joesmith@myneworg.org", sel.get_text("css=search_results .result_row:nth(0) .email"))                


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
    
    
    def test_creating_and_deleting_a_blank_organization(self):
        sel = self.selenium
        self.get_to_organizations_search()
        sel.click("link=New Organization")
        sel.wait_for_page_to_load("30000")
        sel.click("link=Organizations")
        sel.wait_for_page_to_load("30000")

        self.assertEqual("Unnamed Organization", sel.get_text("css=search_results .result_row:nth(0) .name a"))
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "Unnamed Organization")
        sel.key_down("css=#id_search_query","5")
        sel.key_up("css=#id_search_query","5")
        time.sleep(2)
        self.assertEqual("Unnamed Organization", sel.get_text("css=search_results .result_row:nth(0) .name a"))

        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        time.sleep(3)
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.org_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Unnamed Organization from the database? \n\nDeleting will remove this organization and all their data (contact info, employees, etc).  The people associated with this organization will not be removed.\n\nThis action cannot be undone.\n\nPress OK to delete Unnamed Organization.\nPress Cancel to leave things unchanged.")
        sel.click("css=.org_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Unnamed Organization from the database? \n\nDeleting will remove this organization and all their data (contact info, employees, etc).  The people associated with this organization will not be removed.\n\nThis action cannot be undone.\n\nPress OK to delete Unnamed Organization.\nPress Cancel to leave things unchanged.")

        sel.wait_for_page_to_load("30000")
        assert not sel.is_text_present("Unnamed Organization")

    
    def test_creating_and_deleting_a_new_organization(self):
        sel = self.selenium
        self.create_new_organization_and_return_to_search()

        sel.click("link=Organizations")
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





class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, PeopleTestAbstractions, OrganizationsTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["200_test_people.json"]
    
    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
        self.people = [Factory.person(self.account) for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []

    # def tearDown(self):
    #     self.account.delete()
  

    def test_that_blank_organizations_show_at_the_top_of_the_search(self):
        sel = self.selenium
        self.get_to_organizations_search()
        assert not sel.is_text_present("Unnamed Organization")
        sel.click("link=New Organization")
        sel.wait_for_page_to_load("30000")
        # celery catch-up
        time.sleep(5)
        sel.click("link=Organizations")
        sel.wait_for_page_to_load("30000")

        self.assertEqual("Unnamed Organization", sel.get_text("css=search_results .result_row:nth(0) .name a"))

    def test_that_clicking_next_on_the_search_results_works(self):
        sel = self.selenium
        self.get_to_organizations_search()
        first_result = sel.get_text("css=search_results .result_row:nth(0) .name a")
        sel.click("css=.pagination .next")
        sel.wait_for_page_to_load("30000")

        assert first_result != sel.get_text("css=search_results .result_row:nth(0) .name a")


