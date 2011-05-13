#!/bin/bash
aptitude install redis-server
sudo apt-get install -y ruby rubygems ruby1.8-dev ruby1.8 ri1.8 rdoc1.8 irb1.8
sudo apt-get install -y libreadline-ruby1.8 libruby1.8 libopenssl-ruby
sudo apt-get install -y libxslt-dev libxml2-dev
gem install nokogiri
gem install backup
gem install fog

# comment out in /etc/redis/redis.conf
# bind 127.0.0.1