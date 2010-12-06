#Virtualenv setup

directory "/home/mycelium/sites/" do
    owner "mycelium"
    group "mycelium"
    mode 0775
end

virtualenv "/home/mycelium/sites/digitalmycelium.com" do
    owner "mycelium"
    group "mycelium"
    mode 0775
end

directory "/home/mycelium/sites/digitalmycelium.com/run" do
    owner "mycelium"
    group "mycelium"
    mode 0775
end

git "/home/mycelium/sites/digitalmycelium.com/checkouts/digitalmycelium.com" do
  repository "skoczen@skoczen.webfactional.com/home/skoczen/git-root/mycelium.git"
  reference "HEAD"
  user "mycelium"
  group "mycelium"
  action :sync
end

script "Install Requirements" do
  interpreter "bash"
  user "mycelium"
  group "mycelium"
  code <<-EOH
  /home/mycelium/sites/digitalmycelium.com/bin/pip install -r /home/mycelium/sites/digitalmycelium.com/checkouts/digitalmycelium.com/requirements.txt
  EOH
end

# Gunicorn setup

cookbook_file "/etc/init/mycelium-gunicorn.conf" do
    source "gunicorn.conf"
    owner "root"
    group "root"
    mode 0644
    #notifies :restart, resources(:service => "mycelium-gunicorn")
end

cookbook_file "/etc/init/mycelium-celery.conf" do
    source "celery.conf"
    owner "root"
    group "root"
    mode 0644
    #notifies :restart, resources(:service => "mycelium-celery")
end

service "mycelium-gunicorn" do
    provider Chef::Provider::Service::Upstart
    enabled true
    running true
    supports :restart => true, :reload => true, :status => true
    action [:enable, :start]
end

service "mycelium-celery" do
    provider Chef::Provider::Service::Upstart
    enabled true
    running true
    supports :restart => true, :reload => true, :status => true
    action [:enable, :start]
end


cookbook_file "/home/mycelium/.bash_profile" do
    source "bash_profile"
    owner "mycelium"
    group "mycelium"
    mode 0755
end
