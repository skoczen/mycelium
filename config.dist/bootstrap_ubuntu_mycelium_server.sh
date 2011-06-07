#!/bin/bash
aptitude install -y git python2.7 nginx mercurial libjpeg62 libjpeg62-dev lib-zlib upstart chkconfig python-setuptools python2.7-dev libmysql++-dev htop

easy_install-2.7 pip
echo 'VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7' >> ~/.profile
source ~/.profile
mkdir /var/www
rm -rf /var/www/*
pip install --upgrade pip virtualenv virtualenvwrapper
cd ~;mkdir .virtualenvs
chmod +x /root
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> .profile
source ~/.profile

cd /var/www
git clone http://mycelium.skoczen.webfactional.com/mycelium.git mycelium.git
cd mycelium.git;git checkout live
cat /var/www/mycelium.git/config.dist/authorized_keys >> ~/.ssh/authorized_keys

mkvirtualenv --no-site-packages --python=/usr/bin/python2.7 mycelium
echo 'cd /var/www/mycelium.git' >> ~/.virtualenvs/mycelium/bin/postactivate
workon mycelium
pip install --upgrade pip 
pip install --upgrade mercurial
pip install -r requirements.stable.txt
 
mkdir /var/log/celery
cd /etc/init.d; wget https://github.com/ask/celery/raw/master/contrib/generic-init.d/celeryd --no-check-certificate; chmod +x celeryd
sed '1d' celeryd > celeryd.tmp
echo "# chkconfig: 2345 20 80" > celeryd
echo "# description: The Celery start-stop-script" >> celeryd
cat celeryd.tmp >> celeryd
rm celeryd.tmp
chmod +x celeryd

#ln -s /var/www/mycelium.git/config.dist/celeryd /etc/default/celeryd;chmod +x /etc/default/celeryd
#ln -s  /var/www/mycelium.git/config.dist/gunicorn /etc/init.d/mycelium; chmod +x /etc/init.d/mycelium
mv /etc/init/celeryd.conf /etc/init/celeryd.conf.bak
ln -s /var/www/mycelium.git/config.dist/celeryd-upstart /etc/init/celeryd.conf
mv /etc/init.d/mycelium.conf /etc/init.d/mycelium.conf.bak
ln -s  /var/www/mycelium.git/config.dist/gunicorn-upstart /etc/init.d/mycelium.conf
mv /etc/nginx/nginx.conf /etc/default/nginx.conf.bak
ln -s /var/www/mycelium.git/config.dist/nginx.conf /etc/nginx/nginx.conf
echo "from envs.dev import *" > /var/www/mycelium.git/mycelium/settings.py
groupadd nginx
useradd -g nginx -s /usr/sbin/nologin -m -d /home/nginx nginx
mkdir /usr/local/nginx

chkconfig --add celeryd
# chkconfig --add nginx
chkconfig --add mycelium
service celeryd start
service mycelium start
service nginx start