#!/bin/bash

echo "Load variables from .env..."
source /home/vagrant/app/.env

echo "Install PostgreSQL 9.6..."
PG_VERSION="9.6"
PG_CONF="/etc/postgresql/$PG_VERSION/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -sc)-pgdg main"
sudo apt-get -y -qq update
sudo apt-get -y -qq install postgresql-$PG_VERSION postgresql-client-$PG_VERSION postgresql-contrib-$PG_VERSION

# Create db users and database
sudo su postgres -c "psql -c \"CREATE ROLE vagrant SUPERUSER LOGIN PASSWORD '$POSTGRES_PASSWORD'\" "
sudo su postgres -c "createdb -E UTF8 -T template0 --locale=en_US.utf8 -O vagrant vagrant"
sudo su postgres -c "psql -c \"CREATE ROLE $POSTGRES_USER SUPERUSER LOGIN PASSWORD '$POSTGRES_PASSWORD'\" "
sudo su postgres -c "createdb -E UTF8 -T template0 --locale=en_US.utf8 -O $POSTGRES_USER $POSTGRES_DB"

# Update connection settings so we can connect with pgadmin
echo "Enable listen_addresses in postgresql.conf..."
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '\*'/" /etc/postgresql/9.6/main/postgresql.conf
# Add line to /etc/postgresql/9.6/main/pg_hba.conf
# host     all             all             10.0.2.2/24             md5
echo "Add host to pg_hba.conf..."
sudo echo "host     all             all             10.0.2.2/24             md5" >> /etc/postgresql/9.6/main/pg_hba.conf

echo "Restart PostgreSQL..."
sudo /etc/init.d/postgresql restart
