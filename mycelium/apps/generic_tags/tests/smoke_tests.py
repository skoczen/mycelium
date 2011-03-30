from nose.tools import istest
from qi_toolkit.smoke_tests import *
from test_factory import Factory

# TODO: Abstract this.
@istest
def smoke_test_the_tab():
    p = Factory.person()
    smoke_test('people:tab_contents', reverse_args=(p.pk,), post_data={"tab_name":"#tags"},method="POST")

