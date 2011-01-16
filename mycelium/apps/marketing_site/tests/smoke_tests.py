from nose.tools import istest
from qi_toolkit.smoke_tests import *

@istest
def smoke_test_the_app():
    smoke_test('core:more_menu', check_title=True)
