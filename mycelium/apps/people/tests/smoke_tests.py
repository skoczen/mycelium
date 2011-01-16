from nose.tools import istest
from qi_toolkit.smoke_tests import *
from test_factory import Factory

# TODO: Abstract this.
@istest
def smoke_test_the_app():
    smoke_test('people:search', check_title=True)

@istest
def smoke_test_the_app2():
    f = Factory()
    p = f.person()
    smoke_test('people:person', reverse_args=(p.pk,), check_title=True)

@istest
def smoke_test_the_app3():
    smoke_test('people:search_results')

@istest
def smoke_test_the_app4():
    smoke_test('people:new_person', status_code=302)

@istest
def smoke_test_the_app5():
    f = Factory()
    p = f.person()
    smoke_test('people:person_save_basic', reverse_args=(p.pk,))