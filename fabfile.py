from qi_toolkit.fabbase import *

env.project_name = 'mycelium'
env.virtualenv_name = "mycelium"
env.set_path = ""

# remote config, for webfaction
env.production_hosts = ['skoczen.webfactional.com']
env.staging_hosts = ['skoczen.webfactional.com']
env.remote_app_dir = "mycelium_live"
env.remote_live_dir = "mycelium.git"
env.staging_app_dir = "mycelium_staging"
env.staging_live_dir = "mycelium.git"
