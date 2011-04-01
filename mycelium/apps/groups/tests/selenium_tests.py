# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_tests import PeopleTestAbstractions

class GroupTestAbstractions(object):

    def create_person_and_go_to_donor_tab(self):
        self.create_john_smith()
        self.switch_to_donor_tab()

class TestAgainstNoData(QiConservativeSeleniumTestCase, GroupTestAbstractions, PeopleTestAbstractions):

    def test_that_the_new_group_page_loads(self):
        sel = self.selenium
        sel.open("/people")
        sel.wait_for_page_to_load("30000")
        sel.click("link=New Group")
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("All people who match")

    def test_that_the_group_name_can_be_edited(self, new_name="Super duper test group"):
        sel = self.selenium
        self.test_that_the_new_group_page_loads()
        sel.type("css=#basic_info_form #id_name",new_name)
        time.sleep(4)
        self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.edit_done_btn")
        time.sleep(1)
        self.assertEqual(new_name, sel.get_text("css=#container_id_name .view_field"))



class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, GroupTestAbstractions, PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.people = [Factory.person() for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    




