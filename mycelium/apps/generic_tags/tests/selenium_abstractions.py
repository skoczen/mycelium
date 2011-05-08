import time

class TagTestAbstractions(object):
    def switch_to_tag_tab(self):
        sel = self.selenium
        sel.click("css=.detail_tab[href=#tags]")
        time.sleep(3)

    def create_person_and_go_to_tag_tab(self):
        self.create_john_smith()
        self.switch_to_tag_tab()

    def create_person_and_go_to_manage_tags_page(self):
        sel = self.selenium
        self.create_person_and_go_to_tag_tab()
        self.click_and_wait("css=.manage_tags_btn")
        assert sel.is_text_present("Manage Tags")

    def add_a_new_tag(self, name="Test Tag 1"):
        sel = self.selenium
        sel.type("css=form.new_tag_form:nth(0) .new_tag_name_input",name)
        sel.click("css=form.new_tag_form:nth(0) .tag_add_btn")
        time.sleep(1)
        assert sel.is_text_present(name)
        assert sel.is_element_present("css=fragment[name$=_tags]:nth(0) .checkbox.checked:nth(0) input:checked")
        self.assertEqual(name,sel.get_text("css=fragment[name$=_tags]:nth(0) .checkbox.checked:nth(0) label name"))