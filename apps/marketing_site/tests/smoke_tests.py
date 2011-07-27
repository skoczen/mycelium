# from qi_toolkit.sane_smoke_tests import *
# 
# suite = SmokeTestSuite(fixtures=["marketing_site.json",])
# suite.add_test('marketing_site:home', check_title=True)
# suite.add_test('marketing_site:about_us', check_title=True)
# suite.run_suite()

# from qi_toolkit.smoke_tests import *
# from djangosanetesting.cases import DatabaseTestCase

# class TestSmoke(DatabaseTestCase):
#     fixtures = ["marketing_site_localhost.json"]
    
#     def setUp(self):
#         pass
    
#     def tearDown(self):
#         pass

#     def smoke_test_the_app(*args, **kwargs):
#         smoke_test('marketing_site:home', check_title=True)

#     def smoke_test_the_app2(*args, **kwargs):
#         smoke_test('marketing_site:about_us', check_title=True)
