from qi_toolkit.fabbase import *

setup_env_centos("mycelium","root",
                initial_settings={
                    'staging_hosts':['digitalmycelium.com'],
                    'production_hosts':[
                                        '184.73.193.80', 
                                        '50.17.219.15',
                                        # '50.17.142.184'
                                        ],
                    'production_db_hosts':['ext-mysql.digitalmycelium.com'],
                    'staging_db_hosts':['ext-mysql.agoodcloud.com']
                }, 
                overrides={
                    'git_origin':"http://mycelium.skoczen.webfactional.com/mycelium.git",
                    # 'dry_run':True,
                    'local_working_path':"~/workingCopy/goodcloud",
                },
                )



def dump_marketing_fixture():
    magic_run("%(work_on)s cd %(project_name)s; %(python)s manage.py dumpdata --natural --exclude=contenttypes auth.User marketing_site cms mptt menus text  > %(git_path)s/%(project_name)s/apps/marketing_site/fixtures/marketing_site.json")


def repopulate_search_caches():
    magic_run("%(work_on)s cd %(project_name)s; %(python)s manage.py repopulate_search_caches")