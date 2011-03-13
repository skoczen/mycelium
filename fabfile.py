from qi_toolkit.fabbase import *

setup_env_centos("mycelium","root",
                initial_settings={
                    'staging_hosts':['staging.digitalmycelium.com'],
                    'production_hosts':['digitalmycelium.com'],
                    'production_db_hosts':['ext-mysql.digitalmycelium.com'],
                    'staging_db_hosts':['ext-mysql.staging.digitalmycelium.com']
                }, 
                overrides={
                    'git_origin':"http://mycelium.skoczen.webfactional.com/mycelium.git",
                    # 'dry_run':True,
                    'local_working_path':"~/workingCopy/goodcloud",
                },
                )



def dump_marketing_fixture():
    magic_run("%(work_on)s cd %(project_name)s; %(python)s manage.py dumpdata --natural --exclude=contenttypes auth.User marketing_site cms mptt menus text  > %(git_path)s/%(project_name)s/apps/marketing_site/fixtures/marketing_site.json")


   