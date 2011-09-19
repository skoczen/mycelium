# encoding: utf-8
from functional_tests.selenium_test_case import DjangoFunctionalConservativeSeleniumTestCase
import time
from test_factory import Factory
from people.tests.selenium_abstractions import PeopleTestAbstractions
from groups.tests.selenium_abstractions import GroupTestAbstractions
from django.conf import settings
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from accounts.models import UserAccount
from dashboard.tests.selenium_abstractions import DashboardTestAbstractions
from django.core.cache import cache
    
class TestAgainstLiterallyNoData(DjangoFunctionalConservativeSeleniumTestCase, DashboardTestAbstractions):

    def setUp(self, *args, **kwargs):
        self.a1 = self.setup_for_logged_in_with_no_data()
        cache.clear()
        self.verificationErrors = []
    
    def test_the_nothing_done_on_the_checklist_welcome_text_and_something_done_text(self):
        sel = self.selenium
        UserAccount.objects.filter(account=self.account, access_level__name="Staff").delete()
        UserAccount.objects.filter(account=self.account, access_level__name="Volunteer").delete()
        self.get_to_the_dashboard()
        assert sel.is_text_present("Welcome to your very own GoodCloud")
        self.add_volunteer_shift()
        self.get_to_the_dashboard()
        assert not sel.is_text_present("Welcome to your very own GoodCloud")
        assert sel.is_text_present("Looks like you haven't finished")

class TestAgainstNoData(DjangoFunctionalConservativeSeleniumTestCase, DashboardTestAbstractions):
    # # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.setup_for_logged_in_with_no_data()
        
        self.verificationErrors = []

    def test_that_logging_in_goes_to_the_dashboard(self):
        sel = self.selenium
        assert sel.is_text_present("Hello") or sel.is_text_present("Hi")

    def test_that_saying_yes_to_a_nickname_works(self):
        sel = self.selenium
        self.get_to_the_dashboard()
        full_name = sel.get_text("css=.full_name")
        first_name = full_name[:full_name.find(" ")]
        sel.click("css=.yes_to_nickname")
        time.sleep(2)
        assert sel.is_text_present("Thanks, %s" % (first_name,) )
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Hi %s" % (first_name,) )
        assert not sel.is_element_present("css=.yes_to_nickname")

 
    def test_that_saying_no_and_providing_a_new_nickname_works(self):
        sel = self.selenium
        self.get_to_the_dashboard()
        sel.click("css=.no_to_nickname")
        time.sleep(0.25)
        sel.type("css=#id_new_nickname", "Jessy")
        sel.click("css=.save_new_nickname")
        time.sleep(2)
        assert sel.is_text_present("Thanks, Jessy")
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        assert sel.is_text_present("Hi Jessy!")

    def test_that_the_dashboard_checks_off_appropriately(self):
        sel = self.selenium
        
        self.create_another_account()
        self.get_to_the_dashboard()
        self.assert_challenge_checked("user")

        self.import_contacts()
        self.get_to_the_dashboard()
        self.assert_challenge_checked("import")
        
        self.add_volunteer_shift()
        self.get_to_the_dashboard()
        self.assert_challenge_checked("volunteer")

        self.add_donation()
        self.get_to_the_dashboard()
        self.assert_challenge_checked("donation")

        self.create_tag_and_tag_a_board_member()
        self.get_to_the_dashboard()
        self.assert_challenge_checked("board")

        self.assert_challenge_checked("tags")

        self.create_a_spreadsheet()
        self.get_to_the_dashboard()
        # self.assert_challenge_checked("spreadsheet")

        
        assert sel.is_element_present("css=.challenges_complete_section")

    def test_that_creating_an_account_checks_itself_off(self):
        self.create_another_account()
        self.get_to_the_dashboard()
        self.assert_challenge_checked("user")

    def test_that_hiding_challenges_complete_hides_them(self):
        sel = self.selenium
        self.test_that_the_dashboard_checks_off_appropriately()
        sel.click("css=.hide_challenge_complete_link")
        time.sleep(2)
        sel.refresh()
        sel.wait_for_page_to_load("30000")

        assert not sel.is_element_present("css=.challenges_complete_section")



    def test_upcoming_birthdays_display_on_the_dashboard(self):
        sel = self.selenium
        self.test_that_the_dashboard_checks_off_appropriately()
        self.create_john_smith()
        self.save_a_birthday()
        self.get_to_the_dashboard()
        try:
            assert sel.is_text_present("John Smith")
            assert sel.is_text_present("Apr 9")
        except:
            assert sel.is_text_present("None in the next month!")
        


    def test_that_new_conversations_show_up_on_the_dashboard(self):
        sel = self.selenium
        self.test_that_the_dashboard_checks_off_appropriately()
        self.get_to_the_dashboard()
        assert not sel.is_element_present("css=conversation")
        assert sel.is_text_present("No conversations yet!")
        
        self.create_person_and_go_to_conversation_tab()

        a1, d1 = self.add_a_conversation(body="Text like 123.45", date="3/8/2011")
        self.get_to_the_dashboard()

        assert sel.is_text_present("By the Numbers")
        assert sel.is_text_present("Text like 123.45")
        assert sel.is_element_present("css=conversation")

class TestAgainstGeneratedData(DjangoFunctionalConservativeSeleniumTestCase, DashboardTestAbstractions):
    # selenium_fixtures = ["generic_tags.selenium_fixtures.json",]

    def setUp(self, *args, **kwargs):
        self.a1 = self.create_demo_site()   
        self.verificationErrors = []
    
