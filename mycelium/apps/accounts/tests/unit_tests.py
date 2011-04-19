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
            # print "Starting factory for group %s" % i
            Factory.create_demo_site("test%s" % i, quick=True)
        
        # self.assertEqual("Note", "This test is probably failing because the tagset signals re-call the same function improperly. (no account context?)")
        

    def test_objects_by_account_limits_to_account(self):
        from groups.models import Group
        a1 = Factory.account()
        g1 = Factory.group(account=a1, name="group 1")
        a2 = Factory.account()
        g2 = Factory.group(account=a2, name="group 2")

        request = Dummy()
        request.account = a1
        
        self.assertNotEqual(a1,a2)
        self.assertNotEqual(g1,g2)

        self.assertEqual([g for g in Group.objects_by_account(a1).all()], [g1])
        self.assertEqual([g for g in Group.objects_by_account(request).all()], [g1])
        
        self.assertEqual([g for g in Group.objects_by_account(a2).all()], [g2])
        self.assertEqual([g for g in Group.raw_objects.all()], [g1, g2])


    def test_for_each_account_model_that_creating_some_of_them_makes_them_inaccessible_to_other_accounts(self):
        self.assertEqual(True, "Test written")