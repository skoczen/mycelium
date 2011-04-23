# encoding: utf-8
import time
from test_factory import Factory

class GroupTestAbstractions(object):

    def create_person_and_go_to_donor_tab(self):
        self.create_john_smith()
        self.switch_to_donor_tab()
    
    def create_new_group(self, new_name="Test Group"):
        sel = self.selenium
        self.open("/people")
        sel.wait_for_page_to_load("30000")
        self.click_and_wait("link=New Group")
        sel.type("css=#basic_info_form #id_name",new_name)
        time.sleep(4)
        self.assertEqual("Saved a few seconds ago.", sel.get_text("css=.last_save_time"))
        sel.refresh()
        sel.wait_for_page_to_load("30000")
        sel.click("css=.edit_done_btn")
        time.sleep(1)
        self.assertEqual(new_name, sel.get_text("css=#container_id_name .view_field"))

    def create_new_group_and_return_to_search(self, new_name="Test Group"):
        self.create_new_group(new_name=new_name)
        self.click_and_wait("link=Back to All People and Groups")
    
    def create_a_new_rule(self, left_side="have a General tag that", operator="is exactly", right_side="test tag"):
        sel = self.selenium
        time.sleep(1)
        sel.click("css=.add_new_rule_btn")
        time.sleep(0.25)
        sel.select("css=rule:not(.empty):last left_side select", "label=%s" %left_side)
        sel.select("css=rule:not(.empty):last operator select", "label=%s" %operator)
        sel.type("css=rule:not(.empty):last right_side input", right_side)
        time.sleep(2)

    def create_new_group_with_one_rule(self):
        sel = self.selenium
        self.create_new_group()
        sel.click("css=.start_edit_btn")
        self.create_a_new_rule(left_side="have any tag that",operator="contains",right_side="a")
        