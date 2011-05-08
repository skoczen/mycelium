# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from groups.tests.selenium_abstractions import GroupTestAbstractions
from generic_tags.tests.selenium_abstractions import TagTestAbstractions
from rules.tasks import populate_rule_components_for_an_account



class TestAgainstNoData(QiConservativeSeleniumTestCase, GroupTestAbstractions, PeopleTestAbstractions, AccountTestAbstractions, TagTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_with_no_data()
        populate_rule_components_for_an_account(self.account)
        self.verificationErrors = []

    # def tearDown(self):
    #     self.account.delete()


    def test_that_the_new_group_page_loads(self):
        sel = self.selenium
        self.create_new_group()
        assert sel.is_text_present("the following rules")

    def test_creating_and_deleting_a_new_group(self):
        sel = self.selenium
        self.create_new_group_and_return_to_search()

        self.click_and_wait("link=Groups")
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
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        group_name = sel.get_value("css=.basic_info #id_name");
        sel.click("css=.edit_done_btn")
        time.sleep(1)
        self.assertEqual(group_name,sel.get_text("css=#container_id_name .view_field"))
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        self.assertEqual(group_name,sel.get_value("css=.basic_info #id_name"))
        sel.type("css=.basic_info #id_name", "cool frood group")
        sel.click("css=.edit_done_btn")
        time.sleep(2)
        self.assertEqual("cool frood group",sel.get_text("css=#container_id_name .view_field"))

    def test_that_the_add_and_remove_buttons_show_hide_properly(self):
        sel = self.selenium
        self.create_new_group_with_one_rule()
        assert sel.is_visible("css=.remove_rule_btn")
        assert sel.is_visible("css=.add_new_rule_btn")
        sel.click("css=.edit_done_btn")
        time.sleep(1)
        assert not sel.is_visible("css=.remove_rule_btn")
        assert not sel.is_visible("css=.add_new_rule_btn")
        sel.click("css=.start_edit_btn")
        time.sleep(1)
        assert sel.is_visible("css=.remove_rule_btn")
        assert sel.is_visible("css=.add_new_rule_btn")
        sel.click("css=.edit_done_btn")
        time.sleep(1)
        assert not sel.is_visible("css=.remove_rule_btn")
        assert not sel.is_visible("css=.add_new_rule_btn")


    def test_adding_one_rule_saves_the_rule(self):
        sel = self.selenium
        self.create_new_group_with_one_rule()
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side .view_field"), "have any tag that")
        self.assertEqual(sel.get_text("css=rule:nth(0) operator .view_field"), "contains")
        self.assertEqual(sel.get_text("css=rule:nth(0) right_side .view_field"), "a")

    def test_adding_one_valid_one_invalid_and_one_valid_rule_saves_properly(self):
        sel = self.selenium
        self.create_new_group_with_one_rule()
        self.create_a_new_rule(right_side="")
        time.sleep(1)
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side .view_field"), "have any tag that")
        self.assertEqual(sel.get_text("css=rule:nth(0) operator .view_field"), "contains")
        self.assertEqual(sel.get_text("css=rule:nth(0) right_side .view_field"), "a")
        self.assertEqual(sel.get_text("css=rule:nth(1) left_side .view_field"), "have a General tag that")
        self.assertEqual(sel.get_text("css=rule:nth(1) operator .view_field"), "is exactly")
        self.assertEqual(sel.get_text("css=rule:nth(1) right_side .view_field"), "")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        if sel.is_visible("css=.edit_done_btn"):
            sel.click("css=.edit_done_btn")
            time.sleep(0.25)
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side .view_field"), "have any tag that")
        self.assertEqual(sel.get_text("css=rule:nth(0) operator .view_field"), "contains")
        self.assertEqual(sel.get_text("css=rule:nth(0) right_side .view_field"), "a")
        self.assertEqual(sel.get_text("css=rule:nth(1) left_side .view_field"), "have a General tag that")
        self.assertEqual(sel.get_text("css=rule:nth(1) operator .view_field"), "is exactly")
        self.assertEqual(sel.get_text("css=rule:nth(1) right_side .view_field"), "")

    def test_adding_three_rules_removing_two_adding_one_saves_properly(self):
        sel = self.selenium
        self.create_new_group_with_one_rule()
        self.create_a_new_rule(right_side="")
        self.create_a_new_rule(left_side="have a Donor tag that", right_side="major")
        sel.click("css=rule:not(.empty):last .remove_rule_btn")
        time.sleep(0.1)
        sel.click("css=rule:not(.empty):last .remove_rule_btn")
        time.sleep(0.1)
        self.create_a_new_rule(left_side="have a Volunteer tag that", right_side="weekly")
        time.sleep(0.1)

        # two refreshes because of a race condition between the save and the read
        sel.refresh()
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side .view_field"), "have any tag that")
        self.assertEqual(sel.get_text("css=rule:nth(0) operator .view_field"), "contains")
        self.assertEqual(sel.get_text("css=rule:nth(0) right_side .view_field"), "a")
        self.assertEqual(sel.get_text("css=rule:nth(1) left_side .view_field"), "have a Volunteer tag that")
        self.assertEqual(sel.get_text("css=rule:nth(1) operator .view_field"), "is exactly")
        self.assertEqual(sel.get_text("css=rule:nth(1) right_side .view_field"), "weekly")


    def test_adding_three_rules_removing_the_middle_one_and_adding_one_shows_the_new_one_at_the_bottom(self):
        sel = self.selenium
        self.create_new_group_with_one_rule()
        self.create_a_new_rule(left_side="have a Donor tag that", right_side="major")
        self.create_a_new_rule(left_side="have a Volunteer tag that", right_side="weekly")
        sel.click("css=rule:nth(1) .remove_rule_btn")
        time.sleep(3)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side .view_field"), "have any tag that")
        self.assertEqual(sel.get_text("css=rule:nth(0) operator .view_field"), "contains")
        self.assertEqual(sel.get_text("css=rule:nth(0) right_side .view_field"), "a")
        self.assertEqual(sel.get_text("css=rule:nth(1) left_side .view_field"), "have a Volunteer tag that")
        self.assertEqual(sel.get_text("css=rule:nth(1) operator .view_field"), "is exactly")
        self.assertEqual(sel.get_text("css=rule:nth(1) right_side .view_field"), "weekly")
        sel.click("css=.add_new_rule_btn")
        time.sleep(0.25)
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side .view_field"), "have any tag that")
        self.assertEqual(sel.get_text("css=rule:nth(0) operator .view_field"), "contains")
        self.assertEqual(sel.get_text("css=rule:nth(0) right_side .view_field"), "a")
        self.assertEqual(sel.get_text("css=rule:nth(1) left_side .view_field"), "have a Volunteer tag that")
        self.assertEqual(sel.get_text("css=rule:nth(1) operator .view_field"), "is exactly")
        self.assertEqual(sel.get_text("css=rule:nth(1) right_side .view_field"), "weekly")
        
    
    def test_volunteer_status_shows_a_select(self):
        sel = self.selenium
        self.create_new_group()
        sel.click("css=.add_new_rule_btn")
        time.sleep(0.25)
        sel.select("css=rule:not(.empty):last left_side select", "volunteer status")
        assert sel.is_element_present("css=rule:nth(0) right_side select")

    
    def test_donation_date_shows_a_datefield(self):
        sel = self.selenium
        self.create_new_group()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.click("css=.add_new_rule_btn")
        time.sleep(0.25)
        sel.select("css=rule:not(.empty):last left_side select", "last donation")

        assert sel.is_element_present("css=rule:nth(0) right_side input[type=text]")
        
        assert not sel.is_element_present("css=.ui-datepicker-close")
        sel.click("css=rule:nth(0) right_side input[type=text]")
        time.sleep(3)
        assert sel.is_visible("css=.ui-datepicker-close")


    def test_any_tag_contains_status_shows_a_text_field(self):
        sel = self.selenium
        self.create_new_group()
        sel.click("css=.add_new_rule_btn")
        time.sleep(0.25)
        sel.select("css=rule:not(.empty):last left_side select", "have any tag that")
        assert sel.is_element_present("css=rule:nth(0) right_side input[type=text]")
    

    def test_that_people_do_not_show_in_group_search(self):
        sel = self.selenium
        self.create_john_smith_and_verify()
        self.create_new_group_and_return_to_search(new_name="My New Group")

        sel.type("css=#id_search_query", "john smit")
        time.sleep(3)
        assert not sel.is_text_present("John Smith")
        assert sel.is_text_present("No groups found for search")


    def test_search_results_number_changes_after_add_and_removing_tag(self):
        sel = self.selenium
        self.create_new_group("Test Tag Group")
        sel.click("css=.start_edit_btn")
        self.create_a_new_rule(left_side="have any tag that",operator="contains",right_side="Test Tag 1")
        
        sel.click("link=Groups")
        sel.wait_for_page_to_load("30000")
        sel.type("css=#id_search_query", "Test Tag Group")
        time.sleep(1)
        self.assertEqual(sel.get_text("css=.group_row:nth(0) .name"), "Test Tag Group")
        self.assertEqual(sel.get_text("css=.group_row:nth(0) .num_members"), "0")

        self.create_person_and_go_to_tag_tab()
        self.add_a_new_tag()
        
        sel.click("link=Groups")
        sel.wait_for_page_to_load("30000")
        sel.type("css=#id_search_query", "Test Tag Group")
        time.sleep(1)
        self.assertEqual(sel.get_text("css=.group_row:nth(0) .name"), "Test Tag Group")
        self.assertEqual(sel.get_text("css=.group_row:nth(0) .num_members"), "1")


class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, GroupTestAbstractions, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
        populate_rule_components_for_an_account(self.account)
        self.people = [Factory.volunteer_history(self.account) for i in range(1,Factory.rand_int(30,100))]
        self.verificationErrors = []

    # def tearDown(self):
    #     self.account.delete()
    
    def test_that_blank_groups_show_at_the_top_of_the_search(self):
        sel = self.selenium
        self.open("/")
        self.click_and_wait("link=Groups")
        assert not sel.is_text_present("Unnamed Group")
        sel.click("link=New Group")
        sel.wait_for_page_to_load("30000")
        # celery catch-up
        time.sleep(5)
        self.click_and_wait("link=Back to Groups")
        

        self.assertEqual("Unnamed Group", sel.get_text("css=search_results .result_row:nth(0) .name a"))


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
        self.click_and_wait("link=Back to Groups")

        sel.type("css=#id_search_query", "name!!")
        time.sleep(2)
        self.assertEqual(sel.get_text("css=.result_row:nth(0) .name"),"A Completely Different name!!")


    def test_members_list_and_count_updates_after_rule_added(self):
        sel = self.selenium
        self.create_new_group()
        sel.click("css=.start_edit_btn")
        time.sleep(4)
        start_people_count = sel.get_text("css=fragment[name=group_member_count] .count")
        start_member_list = sel.do_command("getHTML",("css=fragment[name=group_member_list]",))
        self.create_a_new_rule(left_side="last volunteer shift", operator="is before", right_side="02/12/2011")
        time.sleep(5)
        self.assertNotEqual(start_people_count,sel.get_text("css=fragment[name=group_member_count] .count"))
        self.assertNotEqual(start_member_list,sel.do_command("getHTML",("css=fragment[name=group_member_list]",)))


    def test_members_list_and_count_updates_after_rule_change(self):
        sel = self.selenium
        self.test_members_list_and_count_updates_after_rule_added()

        start_people_count = sel.get_text("css=fragment[name=group_member_count] .count")
        start_member_list = sel.do_command("getHTML",("css=fragment[name=group_member_list]",))
        sel.type("css=rule:nth(0) right_side input[type=text]","01/10/2010")
        time.sleep(5)
        self.assertNotEqual(start_people_count,sel.get_text("css=fragment[name=group_member_count] .count"))
        self.assertNotEqual(start_member_list,sel.do_command("getHTML",("css=fragment[name=group_member_list]",)))


    def test_members_list_and_count_updates_after_rule_removed(self):
        sel = self.selenium
        self.create_new_group()
        sel.click("css=.start_edit_btn")

        start_people_count = sel.get_text("css=fragment[name=group_member_count] .count")
        start_member_list = sel.do_command("getHTML",("css=fragment[name=group_member_list]",))
        self.create_a_new_rule(left_side="last volunteer shift", operator="is before", right_side="02/12/2011")
        time.sleep(5)
        self.assertNotEqual(start_people_count,sel.get_text("css=fragment[name=group_member_count] .count"))
        self.assertNotEqual(start_member_list,sel.do_command("getHTML",("css=fragment[name=group_member_list]",)))
        
        sel.click("css=rule:nth(0) .remove_rule_btn")
        time.sleep(5)        
        self.assertEqual(start_people_count,sel.get_text("css=fragment[name=group_member_count] .count"))
        self.assertEqual(start_member_list,sel.do_command("getHTML",("css=fragment[name=group_member_list]",)))
