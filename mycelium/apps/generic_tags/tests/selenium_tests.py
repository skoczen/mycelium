# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_tests import PeopleTestAbstractions

class TagTestAbstractions(object):
    def switch_to_tag_tab(self):
        sel = self.selenium
        sel.click("css=.detail_tab[href=#tags]")
        time.sleep(3)

    def create_person_and_go_to_tag_tab(self):
        self.create_john_smith()
        self.switch_to_tag_tab()

class TestAgainstNoData(QiConservativeSeleniumTestCase, TagTestAbstractions, PeopleTestAbstractions):
    selenium_fixtures = ["selenium_fixtures.json",]

    def test_that_tags_tab_display_and_has_the_three_categories(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        assert sel.is_text_present("General")
        assert sel.is_text_present("Volunteer")
        assert sel.is_text_present("Donor")

    def test_adding_a_new_tag(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=#new_general_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_general_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=general_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=general_tags] .checkbox.checked:nth(0) label name"))

    def test_adding_a_new_tag_to_each_category(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=#new_general_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_general_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=general_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=general_tags] .checkbox.checked:nth(0) label name"))

        sel.type("css=#new_volunteer_tag_form .new_tag_name_input","test tag 2")
        sel.click("css=#new_volunteer_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 2")
        assert sel.is_element_present("css=fragment[name=volunteer_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=volunteer_tags] .checkbox.checked:nth(0) label name"))

        sel.type("css=#new_donor_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_donor_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=donor_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=donor_tags] .checkbox.checked:nth(0) label name"))


    def test_adding_multiple_tags_to_one_category(self, tag_name="general"):
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
        sel.click("css=fragment[name=general_tags] .checkbox:nth(1) input[type=checkbox]")
        time.sleep(1)
        # Make sure it's not checked
        assert not sel.is_element_present("css=fragment[name=general_tags] .checkbox:nth(1) input:checked")
        assert sel.is_element_present("css=fragment[name=general_tags] .checkbox:nth(1) input[type=checkbox]")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=general_tags] .checkbox:nth(1) label name"))
        
        # Make sure that stuck after refresh
        self.js_refresh()
        assert not sel.is_element_present("css=fragment[name=general_tags] .checkbox:nth(1) input:checked")
        assert sel.is_element_present("css=fragment[name=general_tags] .checkbox:nth(1) input[type=checkbox]")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=general_tags] .checkbox:nth(1) label name"))
        
        # Re-check #2
        sel.click("css=fragment[name=general_tags] .checkbox:nth(1) input[type=checkbox]")
        time.sleep(1)
        # Make sure it checked
        assert sel.is_element_present("css=fragment[name=general_tags] .checkbox:nth(1) input[type=checkbox]:checked")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=general_tags] .checkbox:nth(1) label name"))
        
        # Make sure that stuck after refresh
        self.js_refresh()
        assert sel.is_element_present("css=fragment[name=general_tags] .checkbox:nth(1) input[type=checkbox]:checked")
        self.assertEqual("Test Tag 2",sel.get_text("css=fragment[name=general_tags] .checkbox:nth(1) label name"))
        
    def test_checking_two_tags_with_the_same_name_and_different_categories_behave_independently(self):
        # Note - this test relies on the fact that the checked/unchecked tags exist on another person, so they stay in the list.
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=#new_general_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_general_tag_form .tag_add_btn")
        sel.type("css=#new_volunteer_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_volunteer_tag_form .tag_add_btn")
        sel.type("css=#new_donor_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_donor_tag_form .tag_add_btn")
        time.sleep(1)
        
        self.create_person_and_go_to_tag_tab()

        sel.type("css=#new_general_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_general_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=general_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=general_tags] .checkbox.checked:nth(0) label name"))

        sel.type("css=#new_volunteer_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_volunteer_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=volunteer_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=volunteer_tags] .checkbox.checked:nth(0) label name"))

        sel.type("css=#new_donor_tag_form .new_tag_name_input","test tag 1")
        sel.click("css=#new_donor_tag_form .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present("Test Tag 1")
        assert sel.is_element_present("css=fragment[name=donor_tags] .checkbox.checked:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=donor_tags] .checkbox.checked:nth(0) label name"))

        # uncheck the volunteer tag, make sure the other two stay checked.
        sel.click("css=fragment[name=volunteer_tags] .checkbox:nth(0) input[type=checkbox]")
        time.sleep(1)

        assert sel.is_element_present("css=fragment[name=general_tags] .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=general_tags] .checkbox:nth(0) label name"))

        assert not sel.is_element_present("css=fragment[name=volunteer_tags] .checkbox:nth(0) input:checked")
        assert sel.is_element_present("css=fragment[name=volunteer_tags] .checkbox:nth(0) input[type=checkbox]")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=volunteer_tags] .checkbox:nth(0) label name"))

        assert sel.is_element_present("css=fragment[name=donor_tags] .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=donor_tags] .checkbox:nth(0) label name"))

        # check and recheck the donor tag, make sure the other two stay unchanged.
        sel.click("css=fragment[name=donor_tags] .checkbox:nth(0) input[type=checkbox]")
        time.sleep(1)
        assert not sel.is_element_present("css=fragment[name=donor_tags] .checkbox:nth(0) input:checked")
        assert sel.is_element_present("css=fragment[name=donor_tags] .checkbox:nth(0) input[type=checkbox]")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=donor_tags] .checkbox:nth(0) label name"))


        sel.click("css=fragment[name=donor_tags] .checkbox:nth(0) input[type=checkbox]")
        time.sleep(1)

        assert sel.is_element_present("css=fragment[name=general_tags] .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=general_tags] .checkbox:nth(0) label name"))

        assert not sel.is_element_present("css=fragment[name=volunteer_tags] .checkbox:nth(0) input:checked")
        assert sel.is_element_present("css=fragment[name=volunteer_tags] .checkbox:nth(0) input[type=checkbox]")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=volunteer_tags] .checkbox:nth(0) label name"))

        assert sel.is_element_present("css=fragment[name=donor_tags] .checkbox:nth(0) input:checked")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=donor_tags] .checkbox:nth(0) label name"))


    def test_unchecking_a_tag_with_no_other_tags_pulls_it_from_the_list(self):
        sel = self.selenium
        self.test_adding_multiple_tags_to_one_category()

        # Uncheck #2
        sel.click("css=fragment[name=general_tags] .checkbox:nth(1) input[type=checkbox]")
        time.sleep(1)

        # Make sure it fell off the list
        assert not sel.is_element_present("css=fragment[name=general_tags] .checkbox:nth(2)")
        self.assertEqual("Test Tag 1",sel.get_text("css=fragment[name=general_tags] .checkbox:nth(0) label name"))
        self.assertEqual("Test Tag 3",sel.get_text("css=fragment[name=general_tags] .checkbox:nth(1) label name"))

                

    def test_multiple_tags_are_sorted_alphabetically(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.type("css=#new_general_tag_form .new_tag_name_input","test A")
        sel.click("css=#new_general_tag_form .tag_add_btn")
        time.sleep(1)

        sel.type("css=#new_general_tag_form .new_tag_name_input","test B")
        sel.click("css=#new_general_tag_form .tag_add_btn")
        time.sleep(1)

        sel.type("css=#new_general_tag_form .new_tag_name_input","A test")
        sel.click("css=#new_general_tag_form .tag_add_btn")
        time.sleep(1)

        assert sel.is_text_present("Test A")
        assert sel.is_text_present("Test B")
        assert sel.is_text_present("A Test")
        self.assertEqual("A Test",sel.get_text("css=fragment[name=general_tags] .checkbox.checked:nth(0) label name"))
        self.assertEqual("Test A",sel.get_text("css=fragment[name=general_tags] .checkbox.checked:nth(1) label name"))
        self.assertEqual("Test B",sel.get_text("css=fragment[name=general_tags] .checkbox.checked:nth(2) label name"))
        
    def test_that_new_categories_can_be_added(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        sel.click("css=tabbed_box[name=add_a_category]")
        time.sleep(0.5)
        sel.type("css=#new_category #id_name", "Test Category 1")
        sel.click("css=tabbed_box .add_category_btn")
        sel.wait_for_page_to_load("30000")
        self.switch_to_tag_tab()                
        assert sel.is_element_present("css=.people_tags_tab column:nth(3) .detail_header")
        self.assertEqual(sel.get_text("css=.people_tags_tab column:nth(3) .detail_header"),"Test Category 1")


        sel.click("css=tabbed_box[name=add_a_category]")
        time.sleep(0.5)
        sel.type("css=#new_category #id_name", "testcategory2")
        sel.click("css=tabbed_box .add_category_btn")
        sel.wait_for_page_to_load("30000")
        self.switch_to_tag_tab()                
        assert sel.is_element_present("css=.people_tags_tab column:nth(4) .detail_header")
        self.assertEqual(sel.get_text("css=.people_tags_tab column:nth(4) .detail_header"),"testcategory2")


    def test_that_tags_can_be_added_and_removed_from_custom_categories(self):    
        self.test_that_new_categories_can_be_added()
        self.test_adding_multiple_tags_to_one_category(tag_name="testcategory2")


class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, TagTestAbstractions, PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    

