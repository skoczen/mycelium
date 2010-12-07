from qi_toolkit.fabbase import *
from fabric.api import *

env.user = 'root'
env.hosts = ['184.106.151.144']

env.chef_executable = '/var/lib/gems/1.8/bin/chef-solo'

def install_chef():
    sudo('apt-get update', pty=True)
    sudo('apt-get install -y git-core rubygems ruby ruby-dev', pty=True)
    sudo('gem install chef', pty=True)

def sync_config():
    local('rsync -av . %s@%s:/etc/chef' % (env.user, env.hosts[0]))

def update():
    sync_config()
    sudo('cd /etc/chef && %s' % env.chef_executable, pty=True)


def full_deploy():
    ssh_auth_me()
    install_chef()
    sync_config()
    update()

DRY_RUN = True

def setup_env_rackspace(initial_settings={}, overrides={}):
    global env
    env.project_name = "mycelium"
    env.webfaction_user = "mycelium"

    # Custom Config Start
    env.parent = "origin"
    env.working_branch = "master"
    env.live_branch = "live"
    env.python = "python"
    env.is_local = False
    env.local_working_path = "~/workingCopy"
    env.media_dir = "media"

    env.update(initial_settings)

    # semi-automated.  Override this for more complex, multi-server setups, or non-wf installs.
    env.production_hosts = ["root@184.106.151.44"]
    env.webfaction_home = "/home/mycelium/sites/digitalmycelium.com/checkouts/digitalmycelium.com/" % env
    env.git_origin = "http://mycelium.qistaging.com/mycelium.git" % env

    env.staging_hosts = env.production_hosts
    env.virtualenv_name = env.project_name
    env.staging_virtualenv_name = "staging_%(project_name)s" % env
    env.live_app_dir = "%(webfaction_home)s/%(project_name)s_live" % env
    env.live_static_dir = "%(webfaction_home)s/%(project_name)s_static" % env
    env.staging_app_dir = "%(webfaction_home)s/%(project_name)s_staging" % env
    env.staging_static_dir = "%(webfaction_home)s/%(project_name)s_staging_static" % env
    env.virtualenv_path = "/home/mycelium/sites/digitalmycelium.com/lib/python2.6/site-packages/" % env
    env.work_on = "workon %(virtualenv_name)s; " % env
setup_env_rackspace()