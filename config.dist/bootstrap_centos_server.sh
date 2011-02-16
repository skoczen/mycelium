#!/bin/bash
rpm -ivh http://repo.webtatic.com/yum/centos/5/`uname -i`/webtatic-release-5-1.noarch.rpm
yum install --enablerepo=webtatic git
yum install python26 python26-setuptools python26-devel python26-devel.x86_64 mysql-devel.x86_64 sqlite3 gmp rabbitmq-server memcached
# eventually memcached will get its own server, but not right now.
cd /etc/init.d; chkconfig --add memcached
cd /etc/init.d; service memcached start
cd /etc/init.d; wget https://github.com/ask/celery/raw/master/contrib/generic-init.d/celeryd --no-check-certificate; chmod +x celeryd
chkconfig rabbitmq-server on
service rabbitmq-server start
rabbitmqctl add_user mycelium 68WXmV6K49r8veczVaUK
rabbitmqctl add_vhost digitalmycelium
rabbitmqctl set_permissions -p digitalmycelium mycelium ".*" ".*" ".*"
easy_install-2.6 pip
echo 'alias python=python26' >> ~/.bashrc
echo 'VIRTUALENVWRAPPER_PYTHON=/usr/bin/python26' >> ~/.bashrc
source ~/.bashrc
pip install --upgrade pip virtualenv virtualenvwrapper
cd ~;mkdir .virtualenvs
echo 'source /usr/bin/virtualenvwrapper.sh' >> .bashrc
source ~/.bashrc
cd /var/www
git clone http://mycelium.skoczen.webfactional.com/mycelium.git mycelium.git
mkvirtualenv mycelium
echo 'cd /var/www/mycelium.git' >> /root/.virtualenvs/mycelium/bin/postactivate
workon mycelium
pip install -r requirements.txt 
echo 'mysql_config = /usr/bin/mysql_config' >> ~/.virtualenvs/mycelium/build/mysql-python/site.cfg
pip install -r requirements.txt 

# need python manage.py celeryd
mkdir /var/log/celery
cp /var/www/mycelium.git/config.dist/celeryd /etc/default/celeryd
cp /var/www/mycelium.git/config.dist/gunicorn /etc/init.d/mycelium
service celeryd start

cp /var/www/mycelium.git/config.dist/nginx.conf /etc/nginx/nginx.conf
killall -HUP nginx

# and run_gunicorn to be running.
workon mycelium; python /var/www/mycelium.git/mycelium/manage.py run_gunicorn --settings=envs.live --workers=2 --daemon
