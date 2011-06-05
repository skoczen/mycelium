#!/bin/bash
rpm -ivh -y http://repo.webtatic.com/yum/centos/5/`uname -i`/webtatic-release-5-1.noarch.rpm
yum install -y --enablerepo=webtatic git
# poss nginx solution
wget http://dl.iuscommunity.org/pub/ius/stable/Redhat/5/x86_64/epel-release-1-1.ius.el5.noarch.rpm
wget http://dl.iuscommunity.org/pub/ius/stable/Redhat/5/x86_64/ius-release-1.0-6.ius.el5.noarch.rpm
rpm -Uvh epel-release-1-1.ius.el5.noarch.rpm ius-release-1.0-6.ius.el5.noarch.rpm
yum install -y nginx
yum install -y python26 python26-setuptools python26-devel python26-devel.x86_64 mysql-devel.x86_64 sqlite3 memcached hg libjpeg-devel zlib-devel freetype-devel maatkit gcc gcc-c++.x86_64 compat-gcc-34-c++.x86_64 openssl-devel.x86_64 zlib*.x86_64
wget http://www.python.org/ftp/python/2.7/Python-2.7.tar.bz2
tar -xvjf Python-2.7.tar.bz2
cd Python*
./configure --prefix=/opt/python27
make
make install

# eventually memcached will get its own server, but not right now.
cd /etc/init.d; wget https://github.com/ask/celery/raw/master/contrib/generic-init.d/celeryd --no-check-certificate; chmod +x celeryd
sed '1d' celeryd > celeryd.tmp
echo "# chkconfig: 2345 20 80" > celeryd
echo "# description: The Celery start-stop-script" >> celeryd
cat celeryd.tmp >> celeryd
rm celeryd.tmp
easy_install-2.6 pip
# echo 'alias python=python26' >> ~/.bashrc
echo 'VIRTUALENVWRAPPER_PYTHON=/opt/python27/bin/python26' >> ~/.bashrc
source ~/.bashrc
mkdir /var/www
mkdir /var/backups
pip install --upgrade pip virtualenv virtualenvwrapper
cd ~;mkdir .virtualenvs
chmod +x /root
echo 'source /usr/bin/virtualenvwrapper.sh' >> .bashrc
source ~/.bashrc
cd /var/www
git clone http://mycelium.skoczen.webfactional.com/mycelium.git mycelium.git
cd mycelium.git;git checkout live
cat /var/www/mycelium.git/config.dist/authorized_keys >> ~/.ssh/authorized_keys
mkvirtualenv --no-site-packages --python=/opt/python27/bin/python mycelium
echo 'cd /var/www/mycelium.git' >> ~/.virtualenvs/mycelium/bin/postactivate
workon mycelium
pip install --upgrade pip 
pip install --upgrade mercurial
pip install -r requirements.stable.txt 
echo 'mysql_config = /usr/bin/mysql_config' >> ~/.virtualenvs/mycelium/build/mysql-python/site.cfg
pip install -r requirements.stable.txt 
mkdir /var/log/celery
mv /etc/default/celeryd /etc/default/celeryd.bak
ln -s /var/www/mycelium.git/config.dist/celeryd /etc/default/celeryd;chmod +x /etc/default/celeryd
mv /etc/init.d/mycelium /etc/init.d/mycelium.bak
ln -s  /var/www/mycelium.git/config.dist/gunicorn /etc/init.d/mycelium; chmod +x /etc/init.d/mycelium
mv /etc/nginx/nginx.conf /etc/default/nginx.conf.bak
ln -s /var/www/mycelium.git/config.dist/nginx.conf /etc/nginx/nginx.conf
echo "from envs.dev import *" > /var/www/mycelium.git/mycelium/settings.py
chkconfig --add celeryd
chkconfig --add nginx
chkconfig --add mycelium
service celeryd start
service mycelium start
service nginx start

# one-time thing to be aware of - syncdb has to be run once with CELERY_RESULT_BACKEND = "database", or dumpdata fails.
