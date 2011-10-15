from functional_tests.selenium_test_case import DjangoFunctionalConservativeSeleniumTestCase
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from spreadsheets.tests.selenium_abstractions import SpreadsheetTestAbstractions
import time
from django.core.cache import cache

class TestSpreadsheets(DjangoFunctionalConservativeSeleniumTestCase, SpreadsheetTestAbstractions, AccountTestAbstractions):
    selenium_fixtures = []

    def setUp(self, *args, **kwargs):
        cache.clear()
        self.account = self.setup_for_logged_in()
    
    def test_spreadsheet_search_loads(self):
        self.get_to_spreadsheets_page()
        self.assert_on_spreadsheet_search_page()

    def test_clicking_the_new_spreadsheet_button_takes_you_to_a_new_spreadsheet(self):
        self.start_a_new_spreadsheet()

    def test_creating_a_new_spreadsheet_saves(self, spreadsheet_name="My test spreadsheet"):
        sel = self.selenium
        self.create_a_spreadsheet(spreadsheet_name)
    
    def test_changing_the_name_group_and_type_of_a_spreadsheet_works(self):
        sel = self.selenium
        self.test_creating_a_new_spreadsheet_saves()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.type("css=#id_name", "Actually, I decided on a new name.")
        sel.select("css=#id_group", "Board of Directors")
        sel.click("css=label[for=id_spreadsheet_template_2]")
        sel.click("css=label[for=id_default_filetype_1]")
        sel.click("css=.save_and_status_btn")
        time.sleep(2)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Actually, I decided on a new name.")
        assert sel.is_text_present("Board of Directors")
        assert sel.is_text_present("Mailing List")

    def test_that_all_and_only_all_of_the_groups_are_listed(self):
        sel = self.selenium
        self.test_creating_a_new_spreadsheet_saves()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)

        assert sel.is_element_present("css=select#id_group option:nth(5)")

        o0 = sel.get_text("css=#id_group option:nth(0)")
        o1 = sel.get_text("css=#id_group option:nth(1)")
        o2 = sel.get_text("css=#id_group option:nth(2)")
        o3 = sel.get_text("css=#id_group option:nth(3)")
        o4 = sel.get_text("css=#id_group option:nth(4)")
        o5 = sel.get_text("css=#id_group option:nth(5)")
        
        # get options in group dropdown
        sel.click("link=Groups")
        sel.wait_for_page_to_load("30000")

        time.sleep(30)
        # get groups
        self.assertEqual(o0,"All Contacts")
        self.assertEqual(o1,sel.get_text("css=.group_row:nth(0) .name"))
        self.assertEqual(o2,sel.get_text("css=.group_row:nth(1) .name"))
        self.assertEqual(o3,sel.get_text("css=.group_row:nth(2) .name"))
        self.assertEqual(o4,sel.get_text("css=.group_row:nth(3) .name"))
        self.assertEqual(o5,sel.get_text("css=.group_row:nth(4) .name"))
        
    
    def test_that_searching_for_a_spreasheet_works(self):
        sel = self.selenium
        self.test_creating_a_new_spreadsheet_saves()
        sel.click("link=Spreadsheets")
        sel.wait_for_page_to_load("30000")
        sel.type("css=#id_search_query","my test")
        time.sleep(1)
        assert sel.is_element_present("css=.spreadsheet_row")
        self.assertEqual(sel.get_text("css=.spreadsheet_row a b:nth(0)"), "My")
        self.assertEqual(sel.get_text("css=.spreadsheet_row a b:nth(1)"), "test")
        sel.type("css=#id_search_query","my testadsfklj;sa;df")
        time.sleep(1)
        assert not sel.is_element_present("css=.spreadsheet_row")
        
    
    def test_that_deleting_a_spreadsheet_works(self):
        sel = self.selenium
        self.test_creating_a_new_spreadsheet_saves()
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.spreadsheet_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete My test spreadsheet from the database? \n\nDeleting will remove this spreadsheet. It will affect any of the people in the spreadsheet.\n\nIt cannot be undone.\n\nPress OK to delete My test spreadsheet.\nPress Cancel to leave things unchanged.")
        sel.click("css=.spreadsheet_delete_btn")
        sel.wait_for_page_to_load("30000")
        self.assert_on_spreadsheet_search_page()
        assert not sel.is_text_present("My test spreadsheet")
  
    def test_changing_the_file_type_of_a_spreadsheet_works(self):
        sel = self.selenium
        self.test_creating_a_new_spreadsheet_saves()    
        sel.click("css=#id_default_filetype_0")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.file_type .file_type_option.selected .option_name"), "CSV")
        sel.click("css=#id_default_filetype_1")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.file_type .file_type_option.selected .option_name"), "Excel")

        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.click("css=#id_default_filetype_0")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.file_type .file_type_option.selected .option_name"), "CSV")

    
    def test_that_selecting_a_group_shows_how_many_members_it_has(self):
        sel = self.selenium
        self.test_creating_a_new_spreadsheet_saves()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)

        sel.select("css=#id_group ", "index=1")
        time.sleep(5)
        assert sel.is_element_present("css=#id_group_count_with_label")
        num_members = sel.get_text("css=#id_group_count_with_label .number")
        
        # get options in group dropdown
        sel.click("link=Groups")
        sel.wait_for_page_to_load("30000")

        # get groups
        self.assertEqual(num_members,sel.get_text("css=.group_row:nth(0) .num_members"))
        
    def test_changing_the_template_type_of_a_spreadsheet_works(self):
        sel = self.selenium
        self.test_creating_a_new_spreadsheet_saves()    
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)

        sel.click("css=#id_spreadsheet_template_1")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        self.assertEqual(sel.get_text("css=#container_id_spreadsheet_template .file_type_option.selected .option_name"), "Full Contact List")

        sel.click("css=#id_spreadsheet_template_2")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        self.assertEqual(sel.get_text("css=#container_id_spreadsheet_template .file_type_option.selected .option_name"), "Home Mailing List")

        sel.click("css=#id_spreadsheet_template_3")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        self.assertEqual(sel.get_text("css=#container_id_spreadsheet_template .file_type_option.selected .option_name"), "Email List")


        sel.click("css=#id_spreadsheet_template_4")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        self.assertEqual(sel.get_text("css=#container_id_spreadsheet_template .file_type_option.selected .option_name"), "Conversations")

        sel.click("css=#id_spreadsheet_template_5")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        self.assertEqual(sel.get_text("css=#container_id_spreadsheet_template .file_type_option.selected .option_name"), "Donation List")

        sel.click("css=#id_spreadsheet_template_6")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        self.assertEqual(sel.get_text("css=#container_id_spreadsheet_template .file_type_option.selected .option_name"), "Donation Summary")

        sel.click("css=#id_spreadsheet_template_7")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        self.assertEqual(sel.get_text("css=#container_id_spreadsheet_template .file_type_option.selected .option_name"), "Volunteer Shifts")

        sel.click("css=#id_spreadsheet_template_8")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        self.assertEqual(sel.get_text("css=#container_id_spreadsheet_template .file_type_option.selected .option_name"), "Volunteer Hour Summary")

    def test_that_the_quick_download_link_works(self):
        sel = self.selenium
        self.test_creating_a_new_spreadsheet_saves()
        sel.click("link=Spreadsheets")
        sel.wait_for_page_to_load("30000")
        self.assert_on_spreadsheet_search_page()
        sel.click("css=.quick_download_btn")
        time.sleep(5)
        self.assert_on_spreadsheet_search_page()

    def test_that_the_download_button_disables_during_save(self):
        sel = self.selenium
        self.test_clicking_the_new_spreadsheet_button_takes_you_to_a_new_spreadsheet()
        assert sel.is_element_present("css=.download_spreadsheet_btn")
        assert not sel.is_element_present("css=.download_spreadsheet_btn.disabled")
        sel.type("css=#id_name", "test")
        time.sleep(0.1)
        assert sel.is_element_present("css=.download_spreadsheet_btn.disabled")
        time.sleep(5.9)
        assert sel.is_element_present("css=.download_spreadsheet_btn")
        assert not sel.is_element_present("css=.download_spreadsheet_btn.disabled")

    def test_that_downloading_an_empty_excel_spreadsheet_does_not_error(self):
        # assert True == "test written (but it should be!) - need to check that the download is valid"
        sel = self.selenium
        self.test_creating_a_new_spreadsheet_saves()
        sel.click("link=Spreadsheets")
        sel.wait_for_page_to_load("30000")
        self.assert_on_spreadsheet_search_page()
        sel.click("css=.quick_download_btn")
        time.sleep(5)
        self.assert_on_spreadsheet_search_page()

    def test_that_downloading_an_empty_csv_spreadsheet_does_not_error(self):
        # assert True == "test written (but it should be!)"
        sel = self.selenium
        self.test_creating_a_new_spreadsheet_saves()
        sel.click("link=Spreadsheets")
        sel.wait_for_page_to_load("30000")
        self.assert_on_spreadsheet_search_page()
        sel.click("css=.quick_download_btn")
        time.sleep(5)
        self.assert_on_spreadsheet_search_page()

