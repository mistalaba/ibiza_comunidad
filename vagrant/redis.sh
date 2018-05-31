#!/bin/bash

echo "Set up and start Redis..."
cd /tmp
curl -O http://download.redis.io/redis-stable.tar.gz
tar xzvf redis-stable.tar.gz
cd redis-stable
make --silent
sudo make --silent install
sudo mkdir /etc/redis
sudo cp /vagrant_setup/redis.conf /etc/redis
sudo cp /vagrant_setup/redis.conf /etc/redis
sudo cp /vagrant_setup/redis.service /etc/systemd/system/
sudo adduser --system --group --no-create-home redis
sudo mkdir /var/lib/redis
sudo chown redis:redis /var/lib/redis
sudo chmod 770 /var/lib/redis
sudo systemctl enable redis
sudo systemctl start redis
