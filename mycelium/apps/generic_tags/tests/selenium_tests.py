# encoding: utf-8
from functional_tests.selenium_test_case import DjangoFunctionalConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from groups.tests.selenium_tests import GroupTestAbstractions
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from generic_tags.tests.selenium_abstractions import TagTestAbstractions
from django.core.cache import cache

class TestAgainstNoData(DjangoFunctionalConservativeSeleniumTestCase, TagTestAbstractions, GroupTestAbstractions, PeopleTestAbstractions, AccountTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_with_no_data()
        cache.clear()

    # def tearDown(self):
    #     self.account.delete()

    def test_that_tags_tab_display_and_has_the_three_categories(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        assert sel.is_text_present("General")
        assert sel.is_text_present("Volunteer")
        assert sel.is_text_present("Donor")

    def test_adding_a_new_tag(self):
        self.create_person_and_go_to_tag_tab()
        self.add_a_new_tag()

    def test_adding_a_new_tag_to_each_category(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=form.new_tag_form:nth(0) .new_tag_name_input","Test Tag 1")
        sel.click("css=form.new_tag_form:nth(0) .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox.checked:nth(0) label name"))

        sel.type("css=form.new_tag_form:nth(1) .new_tag_name_input","Test Tag 2")
        sel.click("css=form.new_tag_form:nth(1) .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 2")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(1) .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name$=_tags]:nth(1) .checkbox.checked:nth(0) label name"))

        sel.type("css=form.new_tag_form:nth(2) .new_tag_name_input","Test Tag 1")
        sel.click("css=form.new_tag_form:nth(2) .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(2) .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(2) .checkbox.checked:nth(0) label name"))


    def test_adding_multiple_tags_to_one_category(self, tag_num=0):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=form.new_tag_form:nth(%s) .new_tag_name_input" % tag_num,"Test Tag 1")
        sel.click("css=form.new_tag_form:nth(%s) .tag_add_btn" % tag_num)
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(%s) .checkbox.checked:nth(0) input:checked" % tag_num)
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(%s) .checkbox.checked:nth(0) label name" % tag_num))

        sel.type("css=form.new_tag_form:nth(%s) .new_tag_name_input" % tag_num,"Test Tag 2")
        sel.click("css=form.new_tag_form:nth(%s) .tag_add_btn" % tag_num)
        time.sleep(1)
        assert sel.is_text_present("Test Tag 2")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(%s) .checkbox.checked:nth(1) input:checked" % tag_num)
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name$=_tags]:nth(%s) .checkbox.checked:nth(1) label name" % tag_num))

        sel.type("css=form.new_tag_form:nth(%s) .new_tag_name_input" % tag_num,"Test Tag 3")
        sel.click("css=form.new_tag_form:nth(%s) .tag_add_btn" % tag_num)
        time.sleep(1)
        assert sel.is_text_present("Test Tag 3")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(%s) .checkbox.checked:nth(2) input:checked" % tag_num)
        self.assertEqual("Test Tag 3",sel.get_text("css=fragment[name$=_tags]:nth(%s) .checkbox.checked:nth(2) label name" % tag_num))

    def test_checking_and_unchecking_works_after_refresh(self):
        # Note - this test relies on the fact that the checked/unchecked tags exist on another person, so they stay in the list.
        sel = self.selenium
        self.test_adding_multiple_tags_to_one_category()
        self.test_adding_multiple_tags_to_one_category()

        # Uncheck #2
        sel.click("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) input[type=checkbox]")
        time.sleep(1)
        # Make sure it's not checked
        assert not sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) input:checked")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) input[type=checkbox]")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) label name"))
        
        # Make sure that stuck after refresh
        self.js_refresh()
        assert not sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) input:checked")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) input[type=checkbox]")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) label name"))
        
        # Re-check #2
        sel.click("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) input[type=checkbox]")
        time.sleep(1)
        # Make sure it checked
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) input[type=checkbox]:checked")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) label name"))
        
        # Make sure that stuck after refresh
        self.js_refresh()
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) input[type=checkbox]:checked")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) label name"))
        
    def test_checking_two_tags_with_the_same_name_and_different_categories_behave_independently(self):
        # Note - this test relies on the fact that the checked/unchecked tags exist on another person, so they stay in the list.
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=form.new_tag_form:nth(0) .new_tag_name_input","Test Tag 1")
        sel.click("css=form.new_tag_form:nth(0) .tag_add_btn")
        sel.type("css=form.new_tag_form:nth(1) .new_tag_name_input","Test Tag 1")
        sel.click("css=form.new_tag_form:nth(1) .tag_add_btn")
        sel.type("css=form.new_tag_form:nth(2) .new_tag_name_input","Test Tag 1")
        sel.click("css=form.new_tag_form:nth(2) .tag_add_btn")
        time.sleep(1)
        
        self.create_person_and_go_to_tag_tab()

        sel.type("css=form.new_tag_form:nth(0) .new_tag_name_input","Test Tag 1")
        sel.click("css=form.new_tag_form:nth(0) .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox.checked:nth(0) label name"))

        sel.type("css=form.new_tag_form:nth(1) .new_tag_name_input","Test Tag 1")
        sel.click("css=form.new_tag_form:nth(1) .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(1) .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(1) .checkbox.checked:nth(0) label name"))

        sel.type("css=form.new_tag_form:nth(2) .new_tag_name_input","Test Tag 1")
        sel.click("css=form.new_tag_form:nth(2) .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(2) .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(2) .checkbox.checked:nth(0) label name"))

        # uncheck the volunteer tag, make sure the other two stay checked.
        sel.click("css=fragment[name$=_tags]:nth(1) .checkbox:nth(0) input[type=checkbox]")
        time.sleep(1)

        assert sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox:nth(0) label name"))

        assert not sel.is_element_present("css=fragment[name$=_tags]:nth(1) .checkbox:nth(0) input:checked")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(1) .checkbox:nth(0) input[type=checkbox]")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(1) .checkbox:nth(0) label name"))

        assert sel.is_element_present("css=fragment[name$=_tags]:nth(2) .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(2) .checkbox:nth(0) label name"))

        # check and recheck the donor tag, make sure the other two stay unchanged.
        sel.click("css=fragment[name$=_tags]:nth(2) .checkbox:nth(0) input[type=checkbox]")
        time.sleep(1)
        assert not sel.is_element_present("css=fragment[name$=_tags]:nth(2) .checkbox:nth(0) input:checked")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(2) .checkbox:nth(0) input[type=checkbox]")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(2) .checkbox:nth(0) label name"))


        sel.click("css=fragment[name$=_tags]:nth(2) .checkbox:nth(0) input[type=checkbox]")
        time.sleep(1)

        assert sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox:nth(0) label name"))

        assert not sel.is_element_present("css=fragment[name$=_tags]:nth(1) .checkbox:nth(0) input:checked")
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(1) .checkbox:nth(0) input[type=checkbox]")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(1) .checkbox:nth(0) label name"))

        assert sel.is_element_present("css=fragment[name$=_tags]:nth(2) .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(2) .checkbox:nth(0) label name"))


    def test_unchecking_a_tag_with_no_other_tags_leaves_it_on_the_list(self):
        sel = self.selenium
        self.test_adding_multiple_tags_to_one_category()

        # Uncheck #2
        sel.click("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) input[type=checkbox]")
        time.sleep(1)

        # Make sure it stayed on the list
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox:nth(2)")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox:nth(0) label name"))
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox:nth(1) label name"))
        self.assertEqual("Test Tag 3",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox:nth(2) label name"))

                

    def test_multiple_tags_are_sorted_alphabetically(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=form.new_tag_form:nth(0) .new_tag_name_input","Test A")
        sel.click("css=form.new_tag_form:nth(0) .tag_add_btn")
        time.sleep(1)

        sel.type("css=form.new_tag_form:nth(0) .new_tag_name_input","Test B")
        sel.click("css=form.new_tag_form:nth(0) .tag_add_btn")
        time.sleep(1)

        sel.type("css=form.new_tag_form:nth(0) .new_tag_name_input","A test")
        sel.click("css=form.new_tag_form:nth(0) .tag_add_btn")
        time.sleep(1)

        assert sel.is_text_present("Test A")
        assert sel.is_text_present("Test B")
        assert sel.is_text_present("A test")
        self.assertEqual("A test",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox.checked:nth(0) label name"))
        self.assertEqual("Test A",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox.checked:nth(1) label name"))
        self.assertEqual("Test B",sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox.checked:nth(2) label name"))
        
    def test_that_new_categories_can_be_added(self):
        sel = self.selenium
        self.create_person_and_go_to_manage_tags_page()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.click("css=.add_a_category_btn")
        time.sleep(2)
        sel.type("css=.detail_header:last input", "Test Category 1")
        sel.click("css=.save_and_status_btn")
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
        sel.click("css=.save_and_status_btn")
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
        time.sleep(2)
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
        time.sleep(6)
        sel.refresh()
        sel.wait_for_page_to_load("30000")

        self.assertEqual(sel.get_text("css=.tag_name .view_field"),"really cool tag")

    
    def test_adding_a_tag_via_the_manage_page_shows_up_on_a_person(self):
        sel = self.selenium
        self.test_adding_a_tag_via_the_manage_page()
        self.create_person_and_go_to_tag_tab()
        self.assertEqual(sel.get_text("css=tag:first name"), "really cool tag")

    def test_adding_a_tag_via_the_a_person_shows_up_on_the_manage_page(self):
        sel = self.selenium
        self.test_adding_a_new_tag()
        self.create_person_and_go_to_manage_tags_page()
        self.assertEqual(sel.get_text("css=.tag_name .view_field"),"Test Tag 1")

    def test_adding_several_tags_via_the_manage_page(self):
        sel = self.selenium
        self.test_adding_a_tag_via_the_manage_page()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)

        sel.click("css=.add_a_tag_btn:first")
        time.sleep(4)
        sel.type("css=.tag_name:nth(1) .generic_editable_field .edit_field input","numero dos tag")
        sel.click("css=.tag_name:nth(1) .generic_editable_field .edit_field input")
        # time.sleep(4)
        sel.click("css=.add_a_tag_btn:first")
        time.sleep(4)
        sel.type("css=.tag_name:nth(2) .generic_editable_field .edit_field input","tag three")
        sel.click("css=.tag_name:nth(2) .generic_editable_field .edit_field input")
        time.sleep(4)
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
        self.open_window("/people/", "two")

        sel.select_window("two")
        self.create_person_and_go_to_tag_tab()
        sel.click("css=.checkbox:nth(0) input[type=checkbox]")
        time.sleep(2)

        # verify
        sel.select_window("")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.tag_row .count"),"1")


        # rinse & repeat for two more
        sel.select_window("two")
        self.create_person_and_go_to_tag_tab()
        sel.click("css=.checkbox:nth(0) input[type=checkbox]")
        time.sleep(2)
        self.create_person_and_go_to_tag_tab()
        sel.click("css=.checkbox:nth(0) input[type=checkbox]")
        time.sleep(2)

        sel.select_window("")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.tag_row .count"),"3")


        # remove it from one person
        sel.select_window("two")
        sel.click("css=.checkbox:nth(0) input[type=checkbox]")
        time.sleep(2)

        # verify
        sel.select_window("")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        self.assertEqual(sel.get_text("css=.tag_row .count"),"2")

    def test_that_tags_can_be_added_and_removed_from_custom_categories(self):    
        self.test_that_new_categories_can_be_added()
        self.test_adding_multiple_tags_to_one_category(tag_num=4)


    def test_that_the_manage_tags_link_works_from_the_people_tab(self):
        self.create_person_and_go_to_manage_tags_page()

    def test_that_the_manage_tags_link_works_from_the_more_page(self):
        sel = self.selenium
        self.open("/people")
        self.click_and_wait("css=.admin_btn")
        self.click_and_wait("css=.tag_button")
        assert sel.is_text_present("Manage Tags")

    def test_deleting_a_custom_tag_group_removes_it_from_rules(self):
        sel = self.selenium
        self.test_that_new_categories_can_be_added()

        self.open_window("/people/", "two")
        sel.select_window("two")        
        self.create_new_group_with_one_rule()
        
        assert sel.is_element_present("css=rule:nth(0) left_side option:nth(7)")
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side option:nth(0)"), "---------")
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side option:nth(7)"), "have a testcategory2 tag that")

        sel.select_window("")
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.click("css=.delete_tagset_btn:last")
        sel.get_confirmation()
        time.sleep(2)

        sel.select_window("two")
        sel.refresh()
        sel.wait_for_page_to_load("3000")
        assert sel.is_element_present("css=rule:nth(0) left_side option:nth(7)")
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side option:nth(0)"), "---------")
        self.assertEqual(sel.get_text("css=rule:nth(0) left_side option:nth(7)"), "volunteer status")
    
    def test_adding_a_tag_via_the_manage_page_creates_a_tag_group(self):
        self.test_adding_a_tag_via_the_manage_page()
        self.ensure_that_a_tag_group_exists_for_a_tag(tag_name="really cool tag")

    def test_adding_a_tag_via_the_person_tag_tab_page_creates_a_tag_group(self):
        self.create_person_and_go_to_tag_tab()
        self.add_a_new_tag()
        self.ensure_that_a_tag_group_exists_for_a_tag()

    def test_removing_a_tag_via_the_manage_page_deletes_the_tag_group(self):
        sel = self.selenium
        self.test_adding_a_tag_via_the_manage_page()
        sel.click("css=.start_edit_btn")
        time.sleep(0.5)
        sel.click("css=.delete_tag_btn:nth(0)")
        self.assertEqual(sel.get_confirmation(),"You sure?\n\nPress OK to delete this tag.\nPress Cancel to leave it in place.")

        self.create_person_and_go_to_tag_tab()
        self.ensure_that_a_tag_group_exists_for_a_tag(tag_name="really cool tag", exists=False)
        

class TestAgainstGeneratedData(DjangoFunctionalConservativeSeleniumTestCase, TagTestAbstractions, PeopleTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
        self.people = [Factory.person(self.account) for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    
    # def tearDown(self):
    #     self.account.delete()

