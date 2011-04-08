# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_tests import PeopleTestAbstractions

class GroupTestAbstractions(object):

    def create_person_and_go_to_donor_tab(self):
        self.create_john_smith()
        self.switch_to_donor_tab()
    
    def create_new_group(self, new_name="Test Group"):
        sel = self.selenium
        sel.open("/people")
        sel.wait_for_page_to_load("30000")
        self.click_and_wait("link=New Group")
        sel.type("css=#basic_info_form #id_name",new_name)
        time.sleep(4)
        self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.edit_done_btn")
        time.sleep(1)
        self.assertEqual(new_name, sel.get_text("css=#container_id_name .view_field"))

    def create_new_group_and_return_to_search(self, new_name="Test Group"):
        self.create_new_group(new_name=new_name)
        self.click_and_wait("link=Back to All People and Groups")

class TestAgainstNoData(QiConservativeSeleniumTestCase, GroupTestAbstractions, PeopleTestAbstractions):

    def test_that_the_new_group_page_loads(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"
        assert sel.is_text_present("the following rules")

    def test_creating_and_deleting_a_new_group(self):
        sel = self.selenium
        self.create_new_group_and_return_to_search()

        self.click_and_wait("link=People")
        sel.wait_for_page_to_load("30000")
        sel.focus("css=#id_search_query")
        sel.type("css=#id_search_query", "Test Grou")

        time.sleep(3)
        self.assertEqual("Test Group", sel.get_text("css=search_results .result_row:nth(0) .name a"))

        sel.click("css=search_results .result_row:nth(0) .name a")
        sel.wait_for_page_to_load("30000")
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.group_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Test Group from the database? \n\nDeleting will remove this group. It will affect any of the people in the group.\n\nIt cannot be undone.\n\nPress OK to delete Test Group.\nPress Cancel to leave things unchanged.")
        sel.click("css=.group_delete_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to completely delete Test Group from the database? \n\nDeleting will remove this group. It will affect any of the people in the group.\n\nIt cannot be undone.\n\nPress OK to delete Test Group.\nPress Cancel to leave things unchanged.")
        
        sel.wait_for_page_to_load("30000")
        assert not sel.is_text_present("Test Group")

    def test_that_the_edit_toggle_works(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"

    def test_that_the_add_and_remove_buttons_show_hide_properly(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"

    def test_adding_one_rule_saves_the_rule(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"

    def test_adding_one_valid_one_invalid_and_one_valid_rule_saves_properly(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"

    def test_adding_three_rules_removing_two_adding_one_saves_properly(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"
    
    def test_volunteer_status_shows_a_select(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"
    
    def test_donation_date_shows_a_datefield(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"

    def test_any_tag_contains_status_shows_a_text_field(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"
    
    

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, GroupTestAbstractions, PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    
    def test_that_blank_groups_show_at_the_top_of_the_search(self):
        sel = self.selenium
        sel.open("/people/")
        assert not sel.is_text_present("No Name")
        sel.click("link=New Group")
        sel.wait_for_page_to_load("30000")
        # celery catch-up
        time.sleep(5)
        self.click_and_wait("link=Back to All People and Groups")
        

        self.assertEqual("No Name", sel.get_text("css=search_results .result_row:nth(0) .name a"))


    def test_editing_and_searching_a_group(self):
        sel = self.selenium
        self.create_new_group_and_return_to_search(new_name="My New Group")

        sel.type("css=#id_search_query", "my new gr")
        time.sleep(2)
        self.assertEqual(sel.get_text("css=.result_row:nth(0) .name"),"My New Group")
        self.click_and_wait("css=.result_row:nth(0) a")
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        sel.type("css=#basic_info_form #id_name","A Completely Different name!!")
        time.sleep(4)
        self.click_and_wait("link=Back to All People and Groups")

        sel.type("css=#id_search_query", "name!!")
        time.sleep(2)
        self.assertEqual(sel.get_text("css=.result_row:nth(0) .name"),"A Completely Different name!!")


    def test_members_list_and_count_updates_after_rule_added(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"

    def test_members_list_and_count_updates_after_rule_change(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"

    def test_members_list_and_count_updates_after_rule_removed(self):
        sel = self.selenium
        self.create_new_group()
        assert True == "test written"
