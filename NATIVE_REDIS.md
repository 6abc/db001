# Install
sudo apt install redis-server -y

# Start and Enable Verify Install
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server
redis-cli ping

# Update Config
sudo nano /etc/redis/redis.conf
- bind 127.0.0.1 -::1
+ bind 0.0.0.0
- protected-mode yes
+ protected-mode no
> optional
requirepass your_redis_password

# Restart & Verify Redis
sudo systemctl restart redis-server
sudo systemctl status redis-server

# Allow Firewall
sudo ufw allow 6379/tcp
> sudo ufw allow from 192.168.0.20 to any port 6379
sudo ufw status

# Verify
redis-cli -h 192.168.0.9 ping
> YesPass
redis-cli -h 192.168.0.9 -a your_redis_password ping

# Remote Verify
sudo apt install redis-tools
redis-cli -h 192.168.0.9 ping
> YesPass
redis-cli -h 192.168.0.9 -a your_redis_password ping
