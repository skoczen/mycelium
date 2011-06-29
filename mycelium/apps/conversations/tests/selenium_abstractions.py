import time
from test_factory import Factory


class ConversationTestAbstractions(object):

    def create_person_and_go_to_conversation_tab(self):
        self.create_john_smith()
        self.switch_to_conversation_tab()
    
    def create_person_with_one_conversation(self):
        self.create_person_and_go_to_conversation_tab()
        return self.add_a_conversation()

    def switch_to_conversation_tab(self):
        sel = self.selenium
        sel.click("css=.detail_tab[href=#conversations]")
        time.sleep(1)


    def add_a_conversation(self, body=None, date=None, hour=5, minute=35, ampm="PM", type="in-person"):
        sel = self.selenium
        self.switch_to_conversation_tab()
        if not body:
            body = Factory.rand_str(500)
        if not date:
            d = Factory.rand_date()
            date = "%02d/%02d/%02d" % (d.month, d.day, d.year)

        sel.click("css=tabbed_box[name=add_a_conversation] tab_title")
        sel.type("css=#id_body", body)
        sel.click("css=input[name=conversation_type][value=%s]" % (type,))
        sel.type("css=#id_date_0", date)
        sel.type("css=#id_date_1", hour)
        sel.type("css=#id_date_2", minute)
        sel.select("css=#id_date_3", ampm)
        sel.click("css=tabbed_box[name=add_a_conversation] .add_conversation_btn")
        time.sleep(2)
        return body,date