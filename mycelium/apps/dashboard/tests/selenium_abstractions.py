# encoding: utf-8
import time
from test_factory import Factory

from volunteers.tests.selenium_abstractions import VolunteerTestAbstractions
from donors.tests.selenium_abstractions import DonorTestAbstractions
from generic_tags.tests.selenium_abstractions import TagTestAbstractions
from groups.tests.selenium_abstractions import GroupTestAbstractions
from spreadsheets.tests.selenium_abstractions import SpreadsheetTestAbstractions
from accounts.tests.selenium_abstractions import AccountTestAbstractions
from people.tests.selenium_abstractions import PeopleTestAbstractions
from data_import.tests.selenium_abstractions import DataImportTestAbstractions
from conversations.tests.selenium_abstractions import ConversationTestAbstractions

class DashboardTestAbstractions(PeopleTestAbstractions, VolunteerTestAbstractions, 
                                DonorTestAbstractions, TagTestAbstractions, GroupTestAbstractions, ConversationTestAbstractions,
                                SpreadsheetTestAbstractions, AccountTestAbstractions, DataImportTestAbstractions,):
    
    def get_to_the_dashboard(self):
        sel = self.selenium
        self.open("/dashboard")
        sel.wait_for_page_to_load(30000)
    
    def assert_challenge_checked(self, challenge_type):
        sel = self.selenium
        assert sel.is_element_present("css=challenge.complete.%s" % challenge_type)

            
    def import_contacts(self):
        self.get_to_start_import_page()
        self.upload_person_spreadsheet_successfully()
        
    def add_volunteer_shift(self):
        self.create_new_volunteer_with_one_shift()


    def add_donation(self):
        self.create_person_with_one_donation()


    def create_tag_and_tag_a_board_member(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        self.add_a_new_tag("Board Member")

        self.create_new_group(new_name="Board Members")
        sel.click("css=.start_edit_btn")
        self.create_a_new_rule(left_side="have any tag that", right_side="Board Member")
        time.sleep(3)


    def create_another_account(self):
        self.create_a_new_user_via_manage_accounts()

