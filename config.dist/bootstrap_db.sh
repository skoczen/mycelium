#!/bin/bash
sudo apt-get install -y ruby rubygems ruby1.8-dev ruby1.8 ri1.8 rdoc1.8 irb1.8
sudo apt-get install -y libreadline-ruby1.8 libruby1.8 libopenssl-ruby
sudo apt-get install -y libxslt-dev libxml2-dev
gem install nokogiri
gem install backup
gem install fog

# create db
# CREATE DATABASE /*!32312 IF NOT EXISTS*/ `mycelium` /*!40100 DEFAULT CHARACTER SET utf8 */;

# Staging
# CREATE USER 'myceliumdb'@'%' IDENTIFIED BY 'pK9Xvt5Kv2dSH586cRrgJ'; GRANT ALL PRIVILEGES ON *.* TO 'myceliumdb'@'%' WITH GRANT OPTION; FLUSH PRIVILEGES;
# CREATE USER 'myceliumdb'@'localhost' IDENTIFIED BY 'pK9Xvt5Kv2dSH586cRrgJ'; GRANT ALL PRIVILEGES ON *.* TO 'myceliumdb'@'localhost' WITH GRANT OPTION; FLUSH PRIVILEGES;

# Live
# CREATE USER 'myceliumdb'@'localhost' IDENTIFIED BY 'Q3lg8Af81tj6vr5PdcIs'; GRANT ALL PRIVILEGES ON *.* TO 'myceliumdb'@'localhost' WITH GRANT OPTION; FLUSH PRIVILEGES;
# CREATE USER 'myceliumdb'@'%' IDENTIFIED BY 'Q3lg8Af81tj6vr5PdcIs'; GRANT ALL PRIVILEGES ON *.* TO 'myceliumdb'@'%' WITH GRANT OPTION; FLUSH PRIVILEGES;

# pass changes
# UPDATE mysql.user SET Password=PASSWORD('Q3lg8Af81tj6vr5PdcIs') WHERE User='myceliumdb'; FLUSH PRIVILEGES;

# Update my.cnf with
# default-character-set=utf8 
# default-collation=utf8_general_ci
# default-storage-engine=InnoDB
# init-connect = 'set collation_connection = utf8_unicode_ci;'