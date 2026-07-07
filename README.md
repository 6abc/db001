## Supported Server configs

1. Jenkins
2. PostgreSQL
3. REDIS

## Static IP Address

1. Debian - /etc/dhcpcd.conf
    Find Link :
    ```sh
    ip link show
    ```
    Static Config as per link
    ```sh
    interface enp0s18
    static ip_address=192.168.0.200/24
    static routers=192.168.0.1
    static domain_name_servers=8.8.8.8 1.1.1.1
    ``` 
