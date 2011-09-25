# # from qi_toolkit.sane_smoke_tests import *
# # 
# # f = Factory()
# # p = f.person()
# # 
# # suite = SmokeTestSuite(fixtures=["marketing_site.json",])
# # suite.add_test('people:search', check_title=True)
# # suite.add_test('people:person', reverse_args=(p.pk,), check_title=True)
# # suite.add_test('people:search_results', check_title=True)
# # suite.add_test('people:new_person', status_code=302)
# # suite.add_test('people:person_save_basic', reverse_args=(p.pk,))
# # suite.run_suite()


# from nose.tools import istest
# from qi_toolkit.smoke_tests import *
# from test_factory import Factory

# from nose.tools import istest
# from qi_toolkit.smoke_tests import *
# from test_factory import Factory
# from djangosanetesting.cases import DatabaseTestCase
# from functional_tests.selenium_test_case import DjangoFunctionalUnitTestMixin
# from django.test import TestCase

# class TestPeopleSmoke(TestCase, DjangoFunctionalUnitTestMixin, DatabaseTestCase):

#     def setUp(self):
#         self.account = Factory.create_demo_site("test1", quick=True)
    
#     def smoke_test_the_app(self):
#         smoke_test('people:search', check_title=True)

#     def smoke_test_the_app2(self):
#         p = Factory.person(self.account)
#         smoke_test('people:person', reverse_args=(p.pk,), check_title=True)

#     def smoke_test_the_app3(self):        
#         smoke_test('people:search_results')

#     def smoke_test_the_app4(self):        
#         smoke_test('people:new_person', status_code=302)

#     def smoke_test_the_app5(self):        
#         p = Factory.person(self.account)
#         smoke_test('people:person_save_basic', reverse_args=(p.pk,))