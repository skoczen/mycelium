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

# TODO: Abstract this.
@istest
def smoke_test_the_app():
    
    Factory.create_demo_site(quick=True)
    smoke_test('people:search', check_title=True)

@istest
def smoke_test_the_app2():
    a1 = Factory.create_demo_site(quick=True)
    p = Factory.person(a1)
    smoke_test('people:person', reverse_args=(p.pk,), check_title=True)

@istest
def smoke_test_the_app3():
    Factory.create_demo_site(quick=True)
    smoke_test('people:search_results')

@istest
def smoke_test_the_app4():
    Factory.create_demo_site(quick=True)
    smoke_test('people:new_person', status_code=302)

@istest
def smoke_test_the_app5():
    a1 = Factory.create_demo_site(quick=True)
    p = Factory.person(a1)
    smoke_test('people:person_save_basic', reverse_args=(p.pk,))