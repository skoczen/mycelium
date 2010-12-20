from nose.tools import istest
from qi_toolkit.smoke_tests import *


# Abstract this.
@istest
def smoke_test_the_app():
    smoke_test('people:search')

@istest
def smoke_test_the_app2():
    smoke_test('people:person')

