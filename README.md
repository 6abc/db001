## Supported Server configs

1. Jenkins
2. PostgreSQL
3. REDIS

## Static IP Address

1. Debian - /etc/network/interfaces
    Find Link :
    ```sh
    ip link show
    ```
    Static Config as per link
    ```sh
    interface enp0s3
    static ip_address=192.168.0.200/24
    static routers=192.168.0.1
    ``` 
