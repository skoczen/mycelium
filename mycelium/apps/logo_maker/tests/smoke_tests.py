from nose.tools import istest
from qi_toolkit.smoke_tests import *
from test_factory import Factory

# TODO: Abstract this.
@istest
def smoke_test_the_app():
    smoke_test('logo_maker:list_logos', check_title=True)

@istest
def smoke_test_the_app2():
    # TODO: need a way to test fake images.
    # smoke_test('logo_maker:download_resized', check_title=True, reverse_args=(1,), post_data={"width": 100, "height":100}, method="POST")
    pass

