from nose.tools import istest
from qi_toolkit.smoke_tests import *
from test_factory import Factory

# Abstract this.
@istest
def smoke_test_the_app():
    smoke_test('people:search')

@istest
def smoke_test_the_app2():
    f = Factory()
    p = f.person()
    smoke_test('people:person', reverse_args=(p.pk,))

