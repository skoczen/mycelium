from qi_toolkit.fabbase import *

setup_env_centos("mycelium","root",
                initial_settings={
                    'staging_hosts':['digitalmycelium.com'],
                    'production_hosts':[
                                '50.16.214.46',
                                '50.16.32.186',
                                       ],
                    'production_db_hosts':['ext-mysql.agoodcloud.com'],
                    'staging_db_hosts':['ext-mysql.digitalmycelium.com'],
                    'admin_symlink' : '_admin'
                    'python_version': '2.6',
                }, 
                overrides={
                    'git_origin':"http://mycelium.skoczen.webfactional.com/mycelium.git",
                    # 'dry_run':True,
                    'local_working_path':"~/workingCopy/goodcloud",
                    "staging_virtualenv_name": "mycelium",
                },
                )



def dump_marketing_fixture():
    magic_run("%(work_on)s cd %(project_name)s; %(python)s manage.py dumpdata --natural --indent 4 --exclude=contenttypes marketing_site cms mptt menus text  > %(git_path)s/%(project_name)s/apps/marketing_site/fixtures/marketing_site.json")


def repopulate_search_caches():
    magic_run("%(work_on)s cd %(project_name)s; %(python)s manage.py repopulate_search_caches")

def backup_db():
    magic_run("backup perform --trigger %(project_name)s")