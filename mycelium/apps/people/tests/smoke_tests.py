# from qi_toolkit.sane_smoke_tests import *
# 
# f = Factory()
# p = f.person()
# 
# suite = SmokeTestSuite(fixtures=["marketing_site.json",])
# suite.add_test('people:search', check_title=True)
# suite.add_test('people:person', reverse_args=(p.pk,), check_title=True)
# suite.add_test('people:search_results', check_title=True)
# suite.add_test('people:new_person', status_code=302)
# suite.add_test('people:person_save_basic', reverse_args=(p.pk,))
# suite.run_suite()


from nose.tools import istest
from qi_toolkit.smoke_tests import *
from test_factory import Factory

from nose.tools import istest
from qi_toolkit.smoke_tests import *
from test_factory import Factory
from djangosanetesting.cases import DatabaseTestCase
from qi_toolkit.selenium_test_case import QiUnitTestMixin
from django.test import TestCase

class TestPeopleSmoke(TestCase, QiUnitTestMixin, DatabaseTestCase):

    def setUp(self):
        self.account = Factory.create_demo_site("test1", quick=True)
    
    def smoke_test_the_app():
        smoke_test('people:search', check_title=True)

    def smoke_test_the_app2():
        p = Factory.person(self.account)
        smoke_test('people:person', reverse_args=(p.pk,), check_title=True)

    def smoke_test_the_app3():        
        smoke_test('people:search_results')

    def smoke_test_the_app4():        
        smoke_test('people:new_person', status_code=302)

    def smoke_test_the_app5():        
        p = Factory.person(self.account)
        smoke_test('people:person_save_basic', reverse_args=(p.pk,))