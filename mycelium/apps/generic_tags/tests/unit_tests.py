from test_factory import Factory
from functional_tests.selenium_test_case import QiUnitTestMixin
from django.test import TestCase
from generic_tags.models import TagSet
from generic_tags import BLANK_TAGSET_NAME


class TestTagSetModelFunctions(QiUnitTestMixin, TestCase):

    def test_saving_a_blank_group_gives_it_a_filler_name(self):
        account = Factory.account()
        ts = TagSet.raw_objects.create(account=account)
        self.assertEqual(ts.name,BLANK_TAGSET_NAME)
        ts.name = "foo"
        ts.save()
        self.assertEqual(ts.name,"foo") 
        ts.name = ""
        ts.save()
        self.assertEqual(ts.name,BLANK_TAGSET_NAME)