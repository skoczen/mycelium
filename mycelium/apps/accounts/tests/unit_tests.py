from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase, DestructiveDatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase
from groups.models import Group
from people.models import Person, Organization, Employee
from donors.models import Donor, Donation
from volunteers.models import Volunteer, CompletedShift
from generic_tags.models import TagSet, Tag

class Dummy(object):
    pass

class TestAccountFactory(TestCase, QiUnitTestMixin, DestructiveDatabaseTestCase):
    # fixtures = ["generic_tags.selenium_fixtures.json"]

    def setUp(self):
        pass

    def test_factory_account_can_be_run_multiple_times(self):
        for i in range(0,Factory.rand_int(2,6)):
            Factory.create_demo_site("test%s" % i, quick=True)

        assert True == True # Finished successfully.        

    def test_objects_by_account_limits_to_account(self, model=Group, factory_method=Factory.group):
        a1 = Factory.account()
        g1 = factory_method(account=a1)
        a2 = Factory.account()
        g2 = factory_method(account=a2)

        request = Dummy()
        request.account = a1
        
        self.assertNotEqual(a1,a2)
        self.assertNotEqual(g1,g2)

        self.assertEqual([g for g in model.objects_by_account(a1).all()], [g1])
        self.assertEqual([g for g in model.objects_by_account(request).all()], [g1])
        
        self.assertEqual([g for g in model.objects_by_account(a2).all()], [g2])
        assert [g for g in model.raw_objects.all()] ==  [g1, g2] or [g for g in model.raw_objects.all()] ==  [g2, g1]


    def test_for_each_account_model_that_creating_some_of_them_makes_them_inaccessible_to_other_accounts(self):
        
        self.test_objects_by_account_limits_to_account(Group, Factory.group)
        
        self.test_objects_by_account_limits_to_account(Person, Factory.person)
        self.test_objects_by_account_limits_to_account(Employee, Factory.employee)
        self.test_objects_by_account_limits_to_account(Donor, Factory.donor)
        self.test_objects_by_account_limits_to_account(Donation, Factory.donation)
        self.test_objects_by_account_limits_to_account(Organization, Factory.organization)
        self.test_objects_by_account_limits_to_account(Volunteer, Factory.volunteer)
        self.test_objects_by_account_limits_to_account(TagSet, Factory.tagset)
        self.test_objects_by_account_limits_to_account(Tag, Factory.tag)
        self.test_objects_by_account_limits_to_account(CompletedShift, Factory.completed_volunteer_shift)

