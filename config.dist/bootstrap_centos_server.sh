#!/bin/bash
rpm -ivh -y http://repo.webtatic.com/yum/centos/5/`uname -i`/webtatic-release-5-1.noarch.rpm
yum install -y --enablerepo=webtatic git
yum install -y python26 python26-setuptools python26-devel python26-devel.x86_64 mysql-devel.x86_64 sqlite3 gmp rabbitmq-server memcached nginx hg
# eventually memcached will get its own server, but not right now.
cd /etc/init.d; wget https://github.com/ask/celery/raw/master/contrib/generic-init.d/celeryd --no-check-certificate; chmod +x celeryd
sed '1d' celeryd > celeryd.tmp
echo "# chkconfig: 2345 20 80" > celeryd
echo "# description: The Celery start-stop-script" >> celeryd
cat celeryd.tmp >> celeryd
rm celeryd.tmp
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
mkdir /var/www
mkdir /var/backups
cd /var/www
git clone http://mycelium.skoczen.webfactional.com/mycelium.git mycelium.git
cd mycelium.git;git checkout live
cat /var/www/mycelium.git/config.dist/authorized_keys >> ~/.ssh/authorized_keys
mkvirtualenv mycelium
echo 'cd /var/www/mycelium.git' >> /root/.virtualenvs/mycelium/bin/postactivate
workon mycelium
pip install -r requirements.txt 
echo 'mysql_config = /usr/bin/mysql_config' >> ~/.virtualenvs/mycelium/build/mysql-python/site.cfg
pip install -r requirements.txt 
mkdir /var/log/celery
mv /etc/default/celeryd /etc/default/celeryd.bak
ln -s /var/www/mycelium.git/config.dist/celeryd /etc/default/celeryd;chmod +x /etc/default/celeryd
mv /etc/init.d/mycelium /etc/init.d/mycelium.bak
ln -s  /var/www/mycelium.git/config.dist/gunicorn /etc/init.d/mycelium; chmod +x /etc/init.d/mycelium
mv /etc/nginx/nginx.conf /etc/default/nginx.conf.bak
ln -s /var/www/mycelium.git/config.dist/nginx.conf /etc/nginx/nginx.conf
chkconfig --add memcached
chkconfig --add rabbitmq-server
chkconfig --add celeryd
chkconfig --add nginx
chkconfig --add mycelium
service memcached start
service rabbitmq-server start
service celeryd start
service mycelium start
service nginx start

# one-time thing to be aware of - syncdb has to be run once with CELERY_RESULT_BACKEND = "database", or dumpdata fails.
