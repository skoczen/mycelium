from qi_toolkit.fabbase import *

# From the chef days
# env.user = 'root'
# env.hosts = ['184.106.151.144']
# 
# env.chef_executable = '/var/lib/gems/1.8/bin/chef-solo'
# 
# def install_chef():
#     sudo('apt-get update', pty=True)
#     sudo('apt-get install -y git-core rubygems ruby ruby-dev', pty=True)
#     sudo('gem install chef', pty=True)
# 
# def sync_config():
#     local('rsync -av . %s@%s:/etc/chef' % (env.user, env.hosts[0]))
# 
# def update():
#     sync_config()
#     sudo('cd /etc/chef && %s' % env.chef_executable, pty=True)
# 
# 
# def full_deploy():
#     ssh_auth_me()
#     install_chef()
#     sync_config()
#     update()

setup_env_webfaction("mycelium","skoczen",
                initial_settings={
                    'webfaction_host':'web166.webfaction.com',
                }, 
                overrides={
                    'git_origin':"http://mycelium.skoczen.webfactional.com/mycelium.git",
                    # 'dry_run':True,
                    'local_working_path':"~/workingCopy/goodcloud",
                    'disable_known_hosts': True,
                },
                )



def dump_marketing_fixture():
    magic_run("%(work_on)s cd %(project_name)s; %(python)s manage.py dumpdata --natural --exclude=contenttypes auth.User marketing_site cms mptt menus text  > %(git_path)s/%(project_name)s/apps/marketing_site/fixtures/marketing_site.json")