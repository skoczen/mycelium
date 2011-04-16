from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase

class Dummy(object):
    pass

class TestAccountFactory(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase):
    # fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        pass

    def test_factory_account_can_be_run_multiple_times(self):

        for i in range(0,Factory.rand_int(2,6)):
            print "Starting factory for group %s" % i
            Factory.create_demo_site("test%s" % i, quick=True)
        assert "Note" == "This test is probably failing because the tagset signals re-call the same function improperly. (no account context?)"
        

    def test_for_each_account_model_that_creating_some_of_them_makes_them_inaccessible_to_other_accounts(self):
        assert True == "Test written"