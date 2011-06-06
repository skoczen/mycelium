#!/bin/bash
aptitude install git python2.7 nginx hg libjpeg62 libjpeg62-dev zlib upstart chkconfig python-setuptools python2.7-dev libmysql++-dev
easy_install-2.7 pip
echo 'VIRTUALENVWRAPPER_PYTHON=/usr/bin/python2.7' >> ~/.bashrc
source ~/.bashrc
mkdir /var/www
rm -rf /var/www/*
pip install --upgrade pip virtualenv virtualenvwrapper
cd ~;mkdir .virtualenvs
chmod +x /root
echo 'source /usr/local/bin/virtualenvwrapper.sh' >> .bashrc
source ~/.bashrc

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

ln -s /var/www/mycelium.git/config.dist/celeryd /etc/init.d/celeryd;chmod +x /etc/init.d/celeryd
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