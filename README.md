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
    auto enp0s3
    iface enp0s3 inet static
        address 192.168.1.150
        netmask 255.255.255.0
        gateway 192.168.1.1
        dns-nameservers 8.8.8.8 1.1.1.1
    ``` 
