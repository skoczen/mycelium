# encoding: utf-8
from qi_toolkit.selenium_test_case import QiConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from conversations.tests.selenium_abstractions import ConversationTestAbstractions


class TestAgainstNoData(QiConservativeSeleniumTestCase, ConversationTestAbstractions, PeopleTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in_with_no_data()

    # def tearDown(self):
    #     # self.account.delete()
    #     pass

    def test_that_new_conversations_can_be_added_and_display_properly(self):
        sel = self.selenium        
        self.create_person_and_go_to_conversation_tab()

        a1, d1 = self.add_a_conversation(body="Text like 85.8", date="3/8/2011")

        # make sure recent conversations display cleanly
        self.assertEqual("%s"%a1, sel.get_text("css=.conversation_row:nth(0) .conversation_body"))
        self.assertEqual("March 8, 2011, 5:35 p.m.", sel.get_text("css=.conversation_row:nth(0) .conversation_date"))
        assert sel.is_element_present("css=.conversation_type.in-person")
        
        assert not sel.is_element_present("css=.conversation_type.email")
        a2, d2 = self.add_a_conversation(body="Text like 8.15", date="1/4/2011", hour=11, minute=12, ampm="AM", type="email")
        self.assertEqual("%s"%a2, sel.get_text("css=.conversation_row:nth(1) .conversation_body"))
        self.assertEqual("Jan. 4, 2011, 11:12 a.m.", sel.get_text("css=.conversation_row:nth(1) .conversation_date"))
        # Test type
        assert sel.is_element_present("css=.conversation_type.email")
        
        # Test username
        my_name = sel.get_text("css=.username")
        self.assertEqual("with %s" % my_name, sel.get_text("css=.conversation_staff"))

   
    def test_that_deleting_conversation_works(self):
        sel = self.selenium        
        self.create_person_with_one_conversation()
        a1, d1 = self.add_a_conversation(body="Text like 85.8", date="3/8/2011")
        a2, d2 = self.add_a_conversation(body="Text like 8.15", date="1/4/2011")        

        sel.choose_cancel_on_next_confirmation()
        sel.click("css=.conversation_row:nth(1) .delete_conversation_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to remove this conversation?\n\nPress OK to remove the conversation.\nPress Cancel to leave things as-is.")
        self.assertEqual("%s"%a1, sel.get_text("css=.conversation_row:nth(0) .conversation_body"))
        self.assertEqual("March 8, 2011, 5:35 p.m.", sel.get_text("css=.conversation_row:nth(0) .conversation_date"))

        self.assertEqual("%s"%a2, sel.get_text("css=.conversation_row:nth(1) .conversation_body"))
        self.assertEqual("Jan. 4, 2011, 5:35 p.m.", sel.get_text("css=.conversation_row:nth(1) .conversation_date"))

        sel.click("css=.conversation_row:nth(1) .delete_conversation_btn")
        self.assertEqual(sel.get_confirmation(),"Are you sure you want to remove this conversation?\n\nPress OK to remove the conversation.\nPress Cancel to leave things as-is.")

        time.sleep(5)
        self.assertEqual("%s"%a1, sel.get_text("css=.conversation_row:nth(0) .conversation_body"))
        self.assertEqual("March 8, 2011, 5:35 p.m.", sel.get_text("css=.conversation_row:nth(0) .conversation_date"))


    def test_that_read_more_works(self):
        sel = self.selenium        
        self.create_person_with_one_conversation()

        body_and_dates = []
        for i in range(0,16):
            a1, d1 = self.add_a_conversation(body="This person really likes the number %s." % i, date="3/8/2011")
            body_and_dates.append({'a':a1, 'd':d1})
        
        assert sel.is_text_present("This person really likes the number 15.")
        assert sel.is_text_present("This person really likes the number 14.")
        assert not sel.is_text_present("This person really likes the number 12.")

        sel.click("css=.more_conversations_link")
        time.sleep(1)
        assert sel.is_text_present("This person really likes the number 15.")
        assert sel.is_text_present("This person really likes the number 14.")
        assert sel.is_text_present("This person really likes the number 12.")
        assert not sel.is_text_present("This person really likes the number 1.")
        
        sel.click("css=.more_conversations_link")
        time.sleep(1)
        assert sel.is_text_present("This person really likes the number 15.")
        assert sel.is_text_present("This person really likes the number 14.")
        assert sel.is_text_present("This person really likes the number 12.")
        assert sel.is_text_present("This person really likes the number 1.")
        assert not sel.is_text_present("No more conversations")
        
        sel.click("css=.more_conversations_link")
        time.sleep(1)
        assert sel.is_text_present("No more conversations")


class TestAgainstGeneratedData(QiConservativeSeleniumTestCase, ConversationTestAbstractions, PeopleTestAbstractions, AccountTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.account = self.setup_for_logged_in()
        self.people = [Factory.person(self.account) for i in range(1,Factory.rand_int(30,300))]
        self.verificationErrors = []
    
    # def tearDown(self):
    #     self.account.delete()
