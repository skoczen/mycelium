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

# def ssh_auth_me():
#     my_key = local("cat ~/.ssh/id_dsa.pub")
#     if my_key == "":
#         my_key = local("cat ~/.ssh/id_rsa.pub")        
# 
#     sudo("mkdir ~/.ssh; chmod 700 ~/.ssh; touch ~/.ssh/authorized_keys; chmod 600 ~/.ssh/authorized_keys;")
#     sudo("echo '%s' >> ~/.ssh/authorized_keys" % (my_key))
# 
