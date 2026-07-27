## Supported Server configs

1. Jenkins
2. PostgreSQL
3. REDIS
4. MinIO
5. Docker
6. Cloud Flare SSH Config

## CODE -> GITHUB -> DOCKER HUB -> KUBERNATES -> CLOUDFLARE -> INTERNET 

## Update hostname 
1. Debian - sudo nano /etc/hostname & sudo nano /etc/hosts

## Static IP Address
### Keep DHCP, Reserve the IP in Your Router ⭐ (Best Practice)

                       Internet
                           │
                    Cloudflare Tunnel
                           │
                      Traefik Ingress
                           │
               ┌────────────────────────┐
               │     k3s Cluster        │
               │                        │
               │ Django Pods            │
               │ Celery Workers         │
               └──────────┬─────────────┘
                          │
    ┌─────────────────────┴┐──────────────────┐
    │                      │                  |    
    PostgreSQL VM       Redis VM       MinIO VM (Object Storage)
