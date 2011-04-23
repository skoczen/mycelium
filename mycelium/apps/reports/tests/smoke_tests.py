# from nose.tools import istest
# from qi_toolkit.smoke_tests import *
# from test_factory import Factory
# from djangosanetesting.cases import DatabaseTestCase
# from qi_toolkit.selenium_test_case import QiUnitTestMixin
# from django.test import TestCase

# class TestReports(TestCase, QiUnitTestMixin, DatabaseTestCase):

#     def setUp(self):
#         Factory.create_demo_site("test", quick=True)

#     # TODO: Abstract this.
    
#     def smoke_test_the_search_page(self):
#         smoke_test('reports:search', check_title=True)

    
#     def smoke_test_the_detail_page(self):
#         r = Factory.report()
#         smoke_test('reports:report_detail', reverse_args=(r.pk,), check_title=True)

    
#     def smoke_test_the_new_report_page(self):
#         smoke_test('reports:new_report', check_title=True)


    
#     def smoke_test_demo_report_1(self):
#         smoke_test('reports:report_detail', reverse_args=(1,), check_title=True)
        
    
#     def smoke_test_demo_report_2(self):
#         smoke_test('reports:report_detail', reverse_args=(2,), check_title=True)

    
#     def smoke_test_demo_report_3(self):
#         smoke_test('reports:report_detail', reverse_args=(3,), check_title=True)
