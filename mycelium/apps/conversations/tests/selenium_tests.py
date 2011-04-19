# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time 
from test_factory import Factory

from people.tests.selenium_abstractions import PeopleTestAbstractions

class ConversationTestAbstractions(object):

    def create_person_and_go_to_recent_activity_tab(self):
        sel = self.selenium
        self.create_john_smith()
        sel.click("css=.detail_tab[href=#conversations]")
        time.sleep(1)

class TestAgainstNoData(QiConservativeSeleniumTestCase, ConversationTestAbstractions, PeopleTestAbstractions):



    def test_conversation_tab_is_a_stub(self):
        sel = self.selenium
        self.create_person_and_go_to_recent_activity_tab()
        assert sel.is_text_present("Conversations aren't done yet, but wait until you see them. I mean, wow.")

class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, ConversationTestAbstractions, PeopleTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()
        self.people = [Factory.person(self.a1) for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    

