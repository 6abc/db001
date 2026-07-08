# Install
```sh
sudo apt install redis-server -y
```
# Start and Enable Verify Install
```sh
sudo systemctl enable redis-server
sudo systemctl start redis-server
sudo systemctl status redis-server
redis-cli ping
```
# Update Config
```sh
sudo nano /etc/redis/redis.conf
```
- bind 127.0.0.1 -::1
+ bind 0.0.0.0
- protected-mode yes
+ protected-mode no
> optional
requirepass your_redis_password
# Restart & Verify Redis
```sh
sudo systemctl restart redis-server
sudo systemctl status redis-server
```
# Allow Firewall
```sh
sudo ufw allow 6379/tcp
```
> sudo ufw allow from 192.168.0.20 to any port 6379
sudo ufw status

# Verify
```sh
IP=$(hostname -I | awk '{print $1}')
redis-cli -h "$IP" ping
```
> YesPass
```sh
redis-cli -h 192.168.0.9 -a your_redis_password ping
```
# Remote Verify
```sh
sudo apt install redis-tools
redis-cli -h 192.168.0.9 ping
```
> YesPass
```sh
redis-cli -h 192.168.0.9 -a your_redis_password ping
```
