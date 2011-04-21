# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from groups.tests.selenium_tests import GroupTestAbstractions
from accounts.tests.selenium_abstractions import AccountTestAbstractions

class TagTestAbstractions(object):
    def switch_to_tag_tab(self):
        sel = self.selenium
        sel.click("css=.detail_tab[href=#tags]")
        time.sleep(3)

    def create_person_and_go_to_tag_tab(self):
        self.create_john_smith()
        self.switch_to_tag_tab()

    def create_person_and_go_to_manage_tags_page(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        self.click_and_wait("css=.manage_tags_btn")
        assert sel.is_text_present("Manage Tags")


class TestAgainstNoData(QiConservativeSeleniumTestCase, TagTestAbstractions, GroupTestAbstractions, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_tests_with_no_data()


    def test_that_tags_tab_display_and_has_the_three_categories(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        assert sel.is_text_present("General")
        assert sel.is_text_present("Volunteer")
        assert sel.is_text_present("Donor")

    def test_adding_a_new_tag(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=#new_22_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_22_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=22_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=22_tags] .checkbox.checked:nth(0) label name"))

    def test_adding_a_new_tag_to_each_category(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=#new_22_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_22_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=22_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=22_tags] .checkbox.checked:nth(0) label name"))

        sel.type("css=#new_23_tag_form .new_tag_name_input","test tag 2")
        sel.click("css=#new_23_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 2")
        assert sel.is_element_present("css=fragment[name=23_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=23_tags] .checkbox.checked:nth(0) label name"))

        sel.type("css=#new_24_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_24_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=24_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=24_tags] .checkbox.checked:nth(0) label name"))


    def test_adding_multiple_tags_to_one_category(self, tag_name="22"):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=#new_%s_tag_form .new_tag_name_input" % tag_name,"test tag 1")
        sel.click("css=#new_%s_tag_form .tag_add_btn" % tag_name)
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=%s_tags] .checkbox.checked:nth(0) input:checked" % tag_name)
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=%s_tags] .checkbox.checked:nth(0) label name" % tag_name))

        sel.type("css=#new_%s_tag_form .new_tag_name_input" % tag_name,"test tag 2")
        sel.click("css=#new_%s_tag_form .tag_add_btn" % tag_name)
        time.sleep(1)
        assert sel.is_text_present("Test Tag 2")
        assert sel.is_element_present("css=fragment[name=%s_tags] .checkbox.checked:nth(1) input:checked" % tag_name)
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=%s_tags] .checkbox.checked:nth(1) label name" % tag_name))

        sel.type("css=#new_%s_tag_form .new_tag_name_input" % tag_name,"test tag 3")
        sel.click("css=#new_%s_tag_form .tag_add_btn" % tag_name)
        time.sleep(1)
        assert sel.is_text_present("Test Tag 3")
        assert sel.is_element_present("css=fragment[name=%s_tags] .checkbox.checked:nth(2) input:checked" % tag_name)
        self.assertEqual("Test Tag 3",sel.get_text("css=fragment[name=%s_tags] .checkbox.checked:nth(2) label name" % tag_name))

    def test_checking_and_unchecking_works_after_refresh(self):
        # Note - this test relies on the fact that the checked/unchecked tags exist on another person, so they stay in the list.
        sel = self.selenium
        self.test_adding_multiple_tags_to_one_category()
        self.test_adding_multiple_tags_to_one_category()

        # Uncheck #2
        sel.click("css=fragment[name=22_tags] .checkbox:nth(1) input[type=checkbox]")
        time.sleep(1)
        # Make sure it's not checked
        assert not sel.is_element_present("css=fragment[name=22_tags] .checkbox:nth(1) input:checked")
        assert sel.is_element_present("css=fragment[name=22_tags] .checkbox:nth(1) input[type=checkbox]")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=22_tags] .checkbox:nth(1) label name"))
        
        # Make sure that stuck after refresh
        self.js_refresh()
        assert not sel.is_element_present("css=fragment[name=22_tags] .checkbox:nth(1) input:checked")
        assert sel.is_element_present("css=fragment[name=22_tags] .checkbox:nth(1) input[type=checkbox]")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=22_tags] .checkbox:nth(1) label name"))
        
        # Re-check #2
        sel.click("css=fragment[name=22_tags] .checkbox:nth(1) input[type=checkbox]")
        time.sleep(1)
        # Make sure it checked
        assert sel.is_element_present("css=fragment[name=22_tags] .checkbox:nth(1) input[type=checkbox]:checked")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=22_tags] .checkbox:nth(1) label name"))
        
        # Make sure that stuck after refresh
        self.js_refresh()
        assert sel.is_element_present("css=fragment[name=22_tags] .checkbox:nth(1) input[type=checkbox]:checked")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=22_tags] .checkbox:nth(1) label name"))
        
    def test_checking_two_tags_with_the_same_name_and_different_categories_behave_independently(self):
        # Note - this test relies on the fact that the checked/unchecked tags exist on another person, so they stay in the list.
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=#new_22_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_22_tag_form .tag_add_btn")
        sel.type("css=#new_23_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_23_tag_form .tag_add_btn")
        sel.type("css=#new_24_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_24_tag_form .tag_add_btn")
        time.sleep(1)
        
        self.create_person_and_go_to_tag_tab()

        sel.type("css=#new_22_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_22_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=22_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=22_tags] .checkbox.checked:nth(0) label name"))

        sel.type("css=#new_23_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_23_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=23_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=23_tags] .checkbox.checked:nth(0) label name"))

        sel.type("css=#new_24_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_24_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=24_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=24_tags] .checkbox.checked:nth(0) label name"))

        # uncheck the volunteer tag, make sure the other two stay checked.
        sel.click("css=fragment[name=23_tags] .checkbox:nth(0) input[type=checkbox]")
        time.sleep(1)

        assert sel.is_element_present("css=fragment[name=22_tags] .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=22_tags] .checkbox:nth(0) label name"))

        assert not sel.is_element_present("css=fragment[name=23_tags] .checkbox:nth(0) input:checked")
        assert sel.is_element_present("css=fragment[name=23_tags] .checkbox:nth(0) input[type=checkbox]")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=23_tags] .checkbox:nth(0) label name"))

        assert sel.is_element_present("css=fragment[name=24_tags] .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=24_tags] .checkbox:nth(0) label name"))

        # check and recheck the donor tag, make sure the other two stay unchanged.
        sel.click("css=fragment[name=24_tags] .checkbox:nth(0) input[type=checkbox]")
        time.sleep(1)
        assert not sel.is_element_present("css=fragment[name=24_tags] .checkbox:nth(0) input:checked")
        assert sel.is_element_present("css=fragment[name=24_tags] .checkbox:nth(0) input[type=checkbox]")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=24_tags] .checkbox:nth(0) label name"))


        sel.click("css=fragment[name=24_tags] .checkbox:nth(0) input[type=checkbox]")
        time.sleep(1)

        assert sel.is_element_present("css=fragment[name=22_tags] .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=22_tags] .checkbox:nth(0) label name"))

        assert not sel.is_element_present("css=fragment[name=23_tags] .checkbox:nth(0) input:checked")
        assert sel.is_element_present("css=fragment[name=23_tags] .checkbox:nth(0) input[type=checkbox]")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=23_tags] .checkbox:nth(0) label name"))

        assert sel.is_element_present("css=fragment[name=24_tags] .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=24_tags] .checkbox:nth(0) label name"))


    def test_unchecking_a_tag_with_no_other_tags_leaves_it_on_the_list(self):
        sel = self.selenium
        self.test_adding_multiple_tags_to_one_category()

        # Uncheck #2
        sel.click("css=fragment[name=22_tags] .checkbox:nth(1) input[type=checkbox]")
        time.sleep(1)

        # Make sure it stayed on the list
        assert sel.is_element_present("css=fragment[name=22_tags] .checkbox:nth(2)")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=22_tags] .checkbox:nth(0) label name"))
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=22_tags] .checkbox:nth(1) label name"))
        self.assertEqual("Test Tag 3",sel.get_text("css=fragment[name=22_tags] .checkbox:nth(2) label name"))

                

    def test_multiple_tags_are_sorted_alphabetically(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=#new_22_tag_form .new_tag_name_input","test A")
        sel.click("css=#new_22_tag_form .tag_add_btn")
        time.sleep(1)

        sel.type("css=#new_22_tag_form .new_tag_name_input","test B")
        sel.click("css=#new_22_tag_form .tag_add_btn")
        time.sleep(1)

        sel.type("css=#new_22_tag_form .new_tag_name_input","A test")
        sel.click("css=#new_22_tag_form .tag_add_btn")
        time.sleep(1)

        assert sel.is_text_present("Test A")
        assert sel.is_text_present("Test B")
        assert sel.is_text_present("A Test")
        self.assertEqual("A Test",sel.get_text("css=fragment[name=22_tags] .checkbox.checked:nth(0) label name"))
        self.assertEqual("Test A",sel.get_text("css=fragment[name=22_tags] .checkbox.checked:nth(1) label name"))
        self.assertEqual("Test B",sel.get_text("css=fragment[name=22_tags] .checkbox.checked:nth(2) label name"))
        
    def test_that_new_categories_can_be_added(self):
        sel = self.selenium
        self.create_person_and_go_to_manage_tags_page()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.click("css=.add_a_category_btn")
        time.sleep(2)
        sel.type("css=.detail_header:last input", "Test Category 1")
        time.sleep(5)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_element_present("css=.detail_header:last .view_field")
        self.assertEqual(sel.get_text("css=.detail_header:last .view_field"),"Test Category 1")

        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.click("css=.add_a_category_btn")
        time.sleep(2)
        sel.type("css=.detail_header:last input", "testcategory2")
        time.sleep(5)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_element_present("css=.detail_header:last .view_field")
        self.assertEqual(sel.get_text("css=.detail_header:last .view_field"),"testcategory2")


    def test_deleting_a_category_works(self):
        sel = self.selenium
        self.test_that_new_categories_can_be_added()
        
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.delete_tagset_btn:last")
        self.assertEqual(sel.get_confirmation(),"Hold on there.\n\nThis will delete the entire tag category, including all tags in it!\n\nThis action can not be undone.\n\nPress OK to delete this tag category.\nPress Cancel to leave it intact.")
        sel.click("css=.delete_tagset_btn:last")
        self.assertEqual(sel.get_confirmation(),"Hold on there.\n\nThis will delete the entire tag category, including all tags in it!\n\nThis action can not be undone.\n\nPress OK to delete this tag category.\nPress Cancel to leave it intact.")
        time.sleep(0.1)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_element_present("css=.detail_header:last .view_field")
        self.assertEqual(sel.get_text("css=.detail_header:last .view_field"),"Test Category 1")
                

    def test_adding_a_tag_via_the_manage_page(self):
        sel = self.selenium
        self.create_person_and_go_to_manage_tags_page()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.click("css=.add_a_tag_btn:first")
        time.sleep(2)
        sel.type("css=.tag_name .generic_editable_field .edit_field input","really cool tag")
        sel.click("css=.tag_name .generic_editable_field .edit_field input")
        time.sleep(4)
        sel.refresh()
        sel.wait_for_page_to_load("30000")

        self.assertEqual(sel.get_text("css=.tag_name .view_field"),"really cool tag")

    
    def test_adding_a_tag_via_the_manage_page_shows_up_on_a_person(self):
        sel = self.selenium
        self.test_adding_a_tag_via_the_manage_page()
        self.create_person_and_go_to_tag_tab()
        self.assertEqual(sel.get_text("css=tag:first name"), "Really Cool Tag")

    def test_adding_a_tag_via_the_a_person_shows_up_on_the_manage_page(self):
        sel = self.selenium
        self.test_adding_a_new_tag()
        self.create_person_and_go_to_manage_tags_page()
        self.assertEqual(sel.get_text("css=.tag_name .view_field"),"test tag 1")

    def test_adding_several_tags_via_the_manage_page(self):
        sel = self.selenium
        self.test_adding_a_tag_via_the_manage_page()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)

        sel.click("css=.add_a_tag_btn:first")
        time.sleep(2)
        sel.type("css=.tag_name .generic_editable_field .edit_field input","numero dos tag")
        sel.click("css=.tag_name .generic_editable_field .edit_field input")
        time.sleep(3)
        sel.click("css=.add_a_tag_btn:first")
        time.sleep(2)
        sel.type("css=.tag_name .generic_editable_field .edit_field input","tag three")
        sel.click("css=.tag_name .generic_editable_field .edit_field input")
        time.sleep(3)
        sel.refresh()
        sel.wait_for_page_to_load("30000")

        self.assertEqual(sel.get_text("css=.tag_name:nth(0) .view_field"),"numero dos tag")
        self.assertEqual(sel.get_text("css=.tag_name:nth(1) .view_field"),"really cool tag")
        self.assertEqual(sel.get_text("css=.tag_name:nth(2) .view_field"),"tag three")
        
            
    def test_deleting_a_tag_via_the_manage_page(self):
        sel = self.selenium
        self.test_adding_several_tags_via_the_manage_page()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.delete_tag_btn:nth(1)")
        self.assertEqual(sel.get_confirmation(),"You sure?\n\nPress OK to delete this tag.\nPress Cancel to leave it in place.")
        sel.click("css=.delete_tag_btn:nth(1)")
        self.assertEqual(sel.get_confirmation(),"You sure?\n\nPress OK to delete this tag.\nPress Cancel to leave it in place.")
        time.sleep(0.1)
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.tag_name:nth(0) .view_field"),"numero dos tag")
        self.assertEqual(sel.get_text("css=.tag_name:nth(1) .view_field"),"tag three")

    def test_the_count_of_tags_on_the_manage_page_is_correct(self):
        sel = self.selenium

        # make a tag
        self.test_adding_a_tag_via_the_manage_page()
        
        # assert zero
        self.assertEqual(sel.get_text("css=.tag_row .count"),"0")

        # give it to one person
        sel.open_window("/people/", "two")

        sel.select_window("two")
        self.create_person_and_go_to_tag_tab()
        sel.click("css=.checkbox:nth(0) input[type=checkbox]")

        # verify
        sel.select_window("")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.tag_row .count"),"1")


        # rinse & repeat for two more
        sel.select_window("two")
        self.create_person_and_go_to_tag_tab()
        sel.click("css=.checkbox:nth(0) input[type=checkbox]")
        self.create_person_and_go_to_tag_tab()
        sel.click("css=.checkbox:nth(0) input[type=checkbox]")

        sel.select_window("")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.tag_row .count"),"3")


        # remove it from one person
        sel.select_window("two")
        sel.click("css=.checkbox:nth(0) input[type=checkbox]")

        # verify
        sel.select_window("")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.tag_row .count"),"2")

    def test_that_tags_can_be_added_and_removed_from_custom_categories(self):    
        self.test_that_new_categories_can_be_added()
        self.test_adding_multiple_tags_to_one_category(tag_name="26")


    def test_that_the_manage_tags_link_works_from_the_people_tab(self):
        self.create_person_and_go_to_manage_tags_page()

    def test_that_the_manage_tags_link_works_from_the_more_page(self):
        sel = self.selenium
        self.open("/people")
        self.click_and_wait("link=More")
        self.click_and_wait("css=.tag_button")
        assert sel.is_text_present("Manage Tags")

    def test_deleting_a_custom_tag_group_removes_it_from_rules(self):
        sel = self.selenium
        self.test_that_new_categories_can_be_added()

        sel.open_window("/people/", "two")
        sel.select_window("two")        
        self.create_new_group_with_one_rule()
        assert sel.is_element_present("css=rule:nth(0) left_side option:nth(6)")
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side option:nth(0)"), "---------")
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side option:nth(6)"), "have a testcategory2 tag that")

        sel.select_window("")
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.click("css=.delete_tagset_btn:last")
        sel.get_confirmation()
        time.sleep(2)

        sel.select_window("two")
        sel.refresh()
        sel.wait_for_page_to_load("3000")
        assert sel.is_element_present("css=rule:nth(0) left_side option:nth(6)")
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side option:nth(0)"), "---------")
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side option:nth(6)"), "volunteer status")



class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, TagTestAbstractions, PeopleTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_tests()
        self.people = [Factory.person(self.account) for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    

