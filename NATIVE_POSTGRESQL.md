# Install 
# Fin supported version
apt search postgresql | grep '^postgresql-[0-9]'
# Use supported version as per above command
sudo apt install postgresql-<Version> postgresql-client-<Version> -y
ex : sudo apt install postgresql-16 postgresql-client-16 -y

# Start and Enable Verify Install
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo systemctl status postgresql

# Create database and user {USER=therapy_user | PASS=therapy_pass | DB=therapy_db}
sudo -u postgres psql
> CREATE DATABASE therapy_db;
> CREATE USER therapy_user WITH PASSWORD 'therapy_pass';
> GRANT ALL PRIVILEGES ON DATABASE therapy_db TO therapy_user;
> \c therapy_db
> GRANT ALL ON SCHEMA public TO therapy_user;
> ALTER SCHEMA public OWNER TO therapy_user;
> \q

# Update Config to Allow remote connections
sudo nano /etc/postgresql/<Version>/main/postgresql.conf
- listen_addresses = 'localhost'
+ listen_addresses = '*'

# Configure client authentication
sudo nano /etc/postgresql/<Version>/main/pg_hba.conf
host    all    all    192.168.0.0/24    scram-sha-256
> optional
> host    all    all    192.168.0.20/32    scram-sha-256

# Restart & Verify PostgreSQL [active (exited) - {Normal Behaviour}]
sudo systemctl restart postgresql
sudo systemctl status postgresql
pg_lsclusters

# Allow Firewall
sudo ufw allow 5432/tcp
sudo ufw reload
sudo ufw status

# Remote Verify
sudo apt install postgresql-client -y
psql -h 192.168.0.9 -U therapy_user -d therapy_db
