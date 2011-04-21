# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time 
from test_factory import Factory

from people.tests.selenium_abstractions import PeopleTestAbstractions

class ConversationTestAbstractions(object):

    def create_person_and_go_to_convesrsations_tab(self):
        sel = self.selenium
        self.create_john_smith()
        sel.click("css=.detail_tab[href=#conversations]")
        time.sleep(1)

class TestAgainstNoData(QiConservativeSeleniumTestCase, ConversationTestAbstractions, PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_tests_with_no_data()

    def test_conversation_tab_is_a_stub(self):
        sel = self.selenium
        self.create_person_and_go_to_conversations_tab()
        assert sel.is_text_present("Conversations aren't done yet, but wait until you see them. I mean, wow.")

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, ConversationTestAbstractions, PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_tests()
        self.people = [Factory.person(self.account) for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    

