from bolt.api import *

env.config_file = True
env.colors = True
env.format = True
env.stages = ["staging", "live"]

@hook('config.loaded')
def bootstrap_env():
    env.workon_command = "workon %(project_name)s;" % env.config

def locally_checkout_live():
    local("git checkout live")

def locally_collect_static():
    local("./manage.py collectstatic --noinput", dir=env.config.project_name)

def locally_push_all():
    local("git push --all")

def tag_commit_for_release():
    local("git tag -d {stage}; git tag {stage}; git push --tags")

def syncmedia():
    local("./manage.py syncmedia --settings=envs.{stage}", dir=env.config.project_name)


def services_action(action, services=None):
    for c in env.ctx:
        config = env.get_settings((c,))[0]
        if not services:
            services = config["services"]

        for s in services:
            env(c).run("service %s %s" % (s, action))

def services_stop(*args, **kwargs):
    services_action("stop", *args, **kwargs)

def services_start(*args, **kwargs):
    services_action("start", *args, **kwargs)

def services_restart(*args, **kwargs):
    services_action("restart", *args, **kwargs)

def services_status(*args, **kwargs):
    services_action("status", *args, **kwargs)

@task('app-servers')
def start(service):
    if env.get_settings(env.ctx) == []:
        print "No servers specified."
    else:
        services_action("start", services=[service,])

@task('app-servers')
def stop(service):
    if env.get_settings(env.ctx) == []:
        print "No servers specified."
    else:
        services_action("stop", services=[service,])

@task('app-servers')
def restart(service):
    if env.get_settings(env.ctx) == []:
        print "No servers specified."
    else:
        services_action("restart", services=[service,])

@task('app-servers')
def status(service):
    if env.get_settings(env.ctx) == []:
        print "No servers specified."
    else:
        services_action("status", services=[service,])


@task('app-servers')
def shell():
    """start a shell within the current context"""
    env().shell(format=True)


def stop_gunicorn():
    return services_stop("gunicorn")

def restart_nginx():
    return services_restart("nginx")

@task("db-server-master")
def backup():
    run("backup perform --trigger {project_name}")

@task
def pull():
    run("cd {project_name}.git; git checkout {stage}; git fetch --tags; git pull; git checkout {stage}", custom_env)

def kill_pyc():
    run("cd {project_name}.git;find . -iname '*.pyc' -delete")

def install_requirements():
    env.force_upgrade_string = ""
    if "pip_force_upgrade" in env:
        env.force_upgrade_string = "--upgrade"
    
    env.requirements = "requirements.stable.txt"
    if "pip_unstable" in env:
        env.requirements = "requirements.txt"

    run("{workon_command}; pip install {force_upgrade_string} -q -r {requirements}")

def migrate():
    run("{workon_command}; cd {project_name}; ./manage.py migrate --database=default")

def syncdb():
    run("{workon_command}; cd {project_name}; ./manage.py syncdb --noinput --database=default")

@task
def ls():
    env("app-servers").run("ls")

@task
def sync_media():
    locally_checkout_live()
    locally_collect_static()
    tag_commit_for_release()
    syncmedia()

@task
def deploy(with_downtime=False, with_media=True, with_backup=True):
    
    if with_media:
        sync_media()
    else:
        locally_checkout_live()
    
    locally_push_all()

    if with_backup:
        backup()

    if with_downtime:
        env("app-servers").multirun(stop_gunicorn)

    env("app-servers").multirun(pull)
    env("app-servers").multirun(kill_pyc)
    env("app-servers").multirun(install_requirements)

    env("app-servers-1").syncdb()
    env("app-servers-1").migrate()
    
    env("celery-servers").multirun(pull)    
    env("celery-servers").multirun(services_restart)
    
    if with_downtime:
        env("app-servers").multirun(restart_nginx)
        env("app-servers").multirun(services_start)
    else:
        env("app-servers").multirun(services_restart)



# def dump_marketing_fixture():
#     magic_run("{workon_command} cd {project_name}; {python} manage.py dumpdata --natural --indent 4 --exclude=contenttypes marketing_site cms mptt menus text  > {git_path}/{project_name}/apps/marketing_site/fixtures/marketing_site.json")


# def repopulate_search_caches():
#     magic_run("{workon_command} cd {project_name}; {python} manage.py repopulate_search_caches")

