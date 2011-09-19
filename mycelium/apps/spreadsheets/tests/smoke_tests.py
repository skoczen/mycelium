# from nose.tools import istest
# from qi_toolkit.smoke_tests import *
# from test_factory import Factory
# from djangosanetesting.cases import DatabaseTestCase
# from functional_tests.selenium_test_case import QiUnitTestMixin
# from django.test import TestCase

# class TestReports(TestCase, QiUnitTestMixin, DatabaseTestCase):

#     def setUp(self):
#         Factory.create_demo_site("test", quick=True)

#     # TODO: Abstract this.
    
#     def smoke_test_the_search_page(self):
#         smoke_test('spreadsheets:search', check_title=True)

    
#     def smoke_test_the_detail_page(self):
#         r = Factory.spreadsheet()
#         smoke_test('spreadsheets:spreadsheet', reverse_args=(r.pk,), check_title=True)

    
#     def smoke_test_the_new_spreadsheet_page(self):
#         smoke_test('spreadsheets:new_spreadsheet', check_title=True)


    
#     def smoke_test_demo_spreadsheet_1(self):
#         smoke_test('spreadsheets:spreadsheet', reverse_args=(1,), check_title=True)
        
    
#     def smoke_test_demo_spreadsheet_2(self):
#         smoke_test('spreadsheets:spreadsheet', reverse_args=(2,), check_title=True)

    
#     def smoke_test_demo_spreadsheet_3(self):
#         smoke_test('spreadsheets:spreadsheet', reverse_args=(3,), check_title=True)
