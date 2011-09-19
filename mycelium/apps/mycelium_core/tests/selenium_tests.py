# encoding: utf-8
from functional_tests.selenium_test_case import DjangoFunctionalConservativeSeleniumTestCase
import time 
from test_factory import Factory

from people.tests.selenium_abstractions import PeopleTestAbstractions
from groups.tests.selenium_abstractions import GroupTestAbstractions
from accounts.tests.selenium_abstractions import AccountTestAbstractions

class TestAgainstNoData(DjangoFunctionalConservativeSeleniumTestCase, PeopleTestAbstractions, GroupTestAbstractions, AccountTestAbstractions):
    
    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_with_no_data()

    # def test_404(self):
    #     sel = self.selenium        
    #     sel.open("/dfiua09zjvbnoizllkq3")
    #     sel.wait_for_page_to_load("30000")
    #     assert sel.is_text_present("we don't have that page")

    # def test_500(self):
    #     sel = self.selenium
    #     sel.open("always_500")
    #     sel.wait_for_page_to_load("30000")
    #     assert sel.is_text_present("problems loading that page")

    def test_that_the_top_search_works(self):
        sel = self.selenium
        self.create_john_smith_and_verify()
        self.create_new_group_and_return_to_search(new_name="My New Group")

        sel.type("css=#global_search","john")
        time.sleep(1)
        assert sel.is_element_present("css=.global_results_table .person_row .name")
        self.assertEqual(sel.get_text("css=.global_results_table .person_row .name"),"John Smith")

        sel.type("css=#global_search","my new")
        time.sleep(1)
        assert sel.is_element_present("css=.global_results_table .group_row .name")
        self.assertEqual(sel.get_text("css=.global_results_table .group_row .name"),"My New Group")


        sel.type("css=#global_search","n")
        time.sleep(1)
        assert sel.is_element_present("css=.global_results_table .person_row:nth(0) .name")
        self.assertEqual(sel.get_text("css=.global_results_table .person_row:nth(0) .name"),"John Smith")
        assert sel.is_element_present("css=.global_results_table .person_row:nth(1) .name")
        self.assertEqual(sel.get_text("css=.global_results_table .person_row:nth(1) .name"),"My New Group")

        sel.type("css=#global_search","naopdfj934adsf")
        time.sleep(1)
        assert sel.is_element_present("css=.global_results_table")
        self.assertEqual(sel.get_text("css=.global_results_table"),"No results found for search \"naopdfj934adsf\".")
