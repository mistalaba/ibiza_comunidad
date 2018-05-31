#!/bin/bash

echo "Load variables from .env..."
source /home/vagrant/app/.env

echo "Provisioning virtual machine..."

echo "Update and install python dev tools..."
sudo apt-get -y -qq update
sudo apt-get -y -qq install build-essential python3-dev python3-setuptools
