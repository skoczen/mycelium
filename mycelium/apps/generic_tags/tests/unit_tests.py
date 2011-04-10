from test_factory import Factory
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase
from generic_tags.models import TagSet
from generic_tags import BLANK_TAGSET_NAME


class TestTagSetModelFunctions(QiUnitTestMixin, TestCase):

    def test_saving_a_blank_group_gives_it_a_filler_name(self):
        ts = TagSet.objects.create()
        self.assertEqual(ts.name,BLANK_TAGSET_NAME)
        ts.name = "foo"
        ts.save()
        self.assertEqual(ts.name,"foo") 
        ts.name = ""
        ts.save()
        self.assertEqual(ts.name,BLANK_TAGSET_NAME)