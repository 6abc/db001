# Install 
### Find supported version
```sh
apt search postgresql | grep '^postgresql-[0-9]'
```
### Use supported version as per above command
```sh
# sudo apt install postgresql-<Version> postgresql-client-<Version> -y
sudo apt install postgresql-17 postgresql-client-17 -y
```

### Start and Enable Verify Install
```sh
sudo systemctl enable postgresql
sudo systemctl start postgresql
sudo systemctl status postgresql
```

### Create database and user {USER=therapy_user | PASS=therapy_pass | DB=therapy_db}
```sh
sudo -u postgres psql
```
```sh
> CREATE DATABASE therapy_db;
> CREATE USER therapy_user WITH PASSWORD 'therapy_pass';
> GRANT ALL PRIVILEGES ON DATABASE therapy_db TO therapy_user;
> \c therapy_db
> GRANT ALL ON SCHEMA public TO therapy_user;
> ALTER SCHEMA public OWNER TO therapy_user;
> \q
```

### Update Config to Allow remote connections
```sh
sudo nano /etc/postgresql/<Version>/main/postgresql.conf
```
- listen_addresses = 'localhost'
+ listen_addresses = '*'

### Configure client authentication
```sh
sudo nano /etc/postgresql/<Version>/main/pg_hba.conf
```
```sh
host    all    all    192.168.0.0/24    scram-sha-256
```
> optional
> host    all    all    192.168.0.20/32    scram-sha-256

### Restart & Verify PostgreSQL [active (exited) - {Normal Behaviour}]
```sh
sudo systemctl restart postgresql
sudo systemctl status postgresql
pg_lsclusters
```

### Allow Firewall
```sh
sudo ufw allow 5432/tcp
sudo ufw reload
sudo ufw status
```

### Remote Verify
```sh
sudo apt install postgresql-client -y
psql -h 192.168.0.9 -U therapy_user -d therapy_db
```

### Database Investigation
```sh
\l             - List the databases
\dt            - List all tables in the database.
\d table_name  - Describe a specific table columns and data types.
\dn            - List all schemas.
\q             - Exit the PostgreSQL shell back to Kali Linux.
```
