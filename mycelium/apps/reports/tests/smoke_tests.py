from nose.tools import istest
from qi_toolkit.smoke_tests import *
from test_factory import Factory

# Abstract this.
@istest
def smoke_test_the_app():
    smoke_test('reports:list')

@istest
def smoke_test_the_app2():
    f = Factory()
    r = f.report()
    smoke_test('reports:report_detail', reverse_args=(r.pk,))
