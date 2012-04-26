from fabric.api import *

env.PROJECT_NAME = "goodcloud"
env.VIRTUALENV_NAME = "mycelium"
env.HEROKU_APP_NAME = env.PROJECT_NAME
# If you're using https://github.com/ddollar/heroku-accounts
env.HEROKU_ACCOUNT = "goodcloud"


def run_ve(cmd):
    env.cmd = cmd
    local("source ~/.virtualenvs/%(VIRTUALENV_NAME)s/bin/activate;cd mycelium;%(cmd)s" % env)

def deploy():
    run_ve("./manage.py collectstatic --noinput --settings=envs.live")
    run_ve("./manage.py compress --force --settings=envs.live")
    run_ve("./manage.py sync_static --gzip --expires --settings=envs.live")
    deploy_code()

def deploy_code():
    run_ve("git push heroku feature/heroku:master")
    run_ve("heroku run mycelium/manage.py syncdb")
    run_ve("heroku run mycelium/manage.py migrate")
    run_ve("heroku restart")