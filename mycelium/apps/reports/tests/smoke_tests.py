from nose.tools import istest
from qi_toolkit.smoke_tests import *
from test_factory import Factory

# TODO: Abstract this.
@istest
def smoke_test_the_search_page():
    smoke_test('reports:search', check_title=True)

@istest
def smoke_test_the_detail_page():
    f = Factory()
    r = f.report()
    smoke_test('reports:report_detail', reverse_args=(r.pk,), check_title=True)

@istest
def smoke_test_the_new_report_page():
    smoke_test('reports:new_report', check_title=True)
    


@istest
def smoke_test_demo_report_1():
    smoke_test('reports:report_detail', reverse_args=(1,), check_title=True)
    
@istest
def smoke_test_demo_report_2():
    smoke_test('reports:report_detail', reverse_args=(2,), check_title=True)

@istest
def smoke_test_demo_report_3():
    smoke_test('reports:report_detail', reverse_args=(3,), check_title=True)
