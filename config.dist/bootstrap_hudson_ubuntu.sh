sudo add-apt-repository "deb http://archive.canonical.com/ lucid partner"
sudo apt-get update
sudo apt-get install -y sun-java6-jdk daemon git-core
sudo apt-get install -y --no-install-recommends ant ant-optional
apt-get install -y postgresql mysql-server libpq-dev sqlite3 python-setuptools python-dev build-essential libmysqlclient-dev xvfb firefox htop
# set staging root pword: Q3lg8Af81tj6vr5PdcIs
easy_install pip
/usr/local/bin/pip install --upgrade pip
pip install virtualenv virtualenvwrapper
# copy xvfb.initd
wget -O /tmp/key http://hudson-ci.org/debian/hudson-ci.org.key
sudo apt-key add /tmp/key
wget -O /tmp/hudson.deb http://hudson-ci.org/latest/debian/hudson.deb
sudo dpkg --install /tmp/hudson.deb
sudo /etc/init.d/hudson start
sudo usermod -c Jenkins,,, hudson
service xvfb start
mysqladmin create mycelium -u root -p


# something like:
#cd $WORKSPACE
#virtualenv -q --no-site-packages ve 
#. ./ve/bin/activate
#cd mycelium
#export DISPLAY=:5.0
#pip install -q --upgrade -r ../requirements.txt
#../ve/bin/python manage.py jenkins_with_selenium_tests --settings=envs.jenkins
#deactivate
#rm -rf ../ve
#kill -9 $(ps aux | grep -v grep | grep selenium-server | awk '{print $2}')