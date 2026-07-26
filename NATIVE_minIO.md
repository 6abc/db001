# Native MinIO Installation on Debian 13

## Architecture

                 Proxmox

        ┌─────────────────────┐
        │  Debian 13 VM        │
        ├─────────────────────┤
        │ sda (32 GB)          │
        │  ├─ Debian           │
        │  ├─ systemd          │
        │  └─ MinIO Binary     │
        ├─────────────────────┤
        │ sdb (100 GB)         │
        │  └─ /mnt/minio-data  │
        └─────────────────────┘
                 │
            Port 9000 (API)
            Port 9001 (Console)
                 │
          Django / Kubernetes

Keep the operating system and MinIO data on **separate virtual disks**.

### Example Layout

```text
ash@minio:~$ lsblk

NAME   SIZE MOUNTPOINT
sda     32G
├─sda1 30.3G /
├─sda2    1K
└─sda5  1.7G [SWAP]

sdb    100G
```

| Disk | Purpose |
|------|---------|
| **sda (32 GB)** | Debian Operating System |
| **sdb (100 GB)** | MinIO Object Storage |

This separation provides several advantages:

- OS upgrades cannot affect object storage.
- The data disk can be expanded independently.
- The MinIO data disk can be backed up or migrated separately.
- If Debian must be reinstalled, the data disk can be reattached without copying files.
- Storage can be increased by simply replacing or resizing the data disk.

---

# Step 1 - Add a Virtual Disk

From the Proxmox Web UI:

```
Datacenter
    └── Node
         └── VM
              └── Hardware
                   └── Add
                        └── Hard Disk
```

Recommended settings:

| Setting | Value |
|---------|-------|
| Bus/Device | VirtIO SCSI (recommended) |
| Storage | Your preferred Proxmox storage |
| Disk Size | 100 GB (or larger) |
| Cache | Default |
| Discard | Enabled |
| SSD Emulation | Enabled (recommended for SSD/NVMe storage) |
| Backup | Enabled |

Start the VM (or rescan disks if hot-added).

Verify:

```bash
lsblk
```

Expected:

```text
NAME   SIZE
sda     32G
└─...

sdb    100G
```

At this point, **`/dev/sdb` should be empty** and ready for partitioning.

Proceed to the next step to create a GPT partition table and format the disk.

### Environment

| Component | Value |
|-----------|-------|
| OS | Debian 13 (Trixie) |
| Installation | Native Binary |
| Data Disk | 100 GB |
| Mount Point | /mnt/minio-data |
| API Port | 9000 |
| Console Port | 9001 |

---

# Step 1 - Create MinIO User

```bash
sudo groupadd -r minio
sudo useradd -r -g minio -s /usr/sbin/nologin minio
```

Verify:

```bash
id minio
```

---

# Step 2 - Partition Data Disk

Example disk:

```
/dev/sdb
```

Create GPT and one partition:

```bash
sudo parted /dev/sdb --script mklabel gpt
sudo parted /dev/sdb --script mkpart primary ext4 0% 100%
```

Verify:

```bash
lsblk
```

---

# Step 3 - Format Disk

```bash
sudo mkfs.ext4 -L MINIO_DATA /dev/sdb1
```

---

# Step 4 - Create Mount Point

```bash
sudo mkdir -p /mnt/minio-data
```

---

# Step 5 - Get UUID

```bash
sudo blkid /dev/sdb1
```

Example

```
UUID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

---

# Step 6 - Configure fstab

Edit

```bash
sudo nano /etc/fstab
```

Add

```
UUID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx /mnt/minio-data ext4 defaults,noatime 0 2
```

Reload

```bash
sudo systemctl daemon-reload
sudo mount -a
```

Verify

```bash
df -h
```

---

# Step 7 - Set Permissions

```bash
sudo chown -R minio:minio /mnt/minio-data
sudo chmod 750 /mnt/minio-data
```

---

# Step 8 - Install Dependencies

```bash
sudo apt update

sudo apt install -y \
curl \
wget \
openssl \
jq \
vim \
ca-certificates
```

---

# Step 9 - Download MinIO

```bash
cd /tmp

wget https://dl.min.io/server/minio/release/linux-amd64/minio

chmod +x minio

sudo mv minio /usr/local/bin/
```

Verify

```bash
minio --version
```

---

# Step 10 - Configure MinIO

Create directory

```bash
sudo mkdir -p /etc/minio
```

Generate password

```bash
openssl rand -base64 32
```

Create configuration

```bash
sudo nano /etc/minio/minio.conf
```

```
MINIO_ROOT_USER=minioadmin

MINIO_ROOT_PASSWORD=CHANGE_TO_RANDOM_PASSWORD

MINIO_VOLUMES="/mnt/minio-data"

MINIO_OPTS="--address :9000 --console-address :9001"
```

Secure file

```bash
sudo chown root:minio /etc/minio/minio.conf
sudo chmod 640 /etc/minio/minio.conf
```

---

# Step 11 - Create systemd Service

```bash
sudo nano /etc/systemd/system/minio.service
```

```
[Unit]
Description=MinIO Object Storage
Documentation=https://min.io/docs/minio/linux/index.html
After=network-online.target
Wants=network-online.target

[Service]
User=minio
Group=minio

EnvironmentFile=/etc/minio/minio.conf

ExecStart=/usr/local/bin/minio server $MINIO_VOLUMES $MINIO_OPTS

Restart=always
RestartSec=5

LimitNOFILE=65536

NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=full
ProtectHome=yes
ReadWritePaths=/mnt/minio-data

StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

---

# Step 12 - Start MinIO

```bash
sudo systemctl daemon-reload

sudo systemctl enable minio

sudo systemctl start minio
```

Verify

```bash
systemctl status minio
```

Logs

```bash
journalctl -u minio -f
```

---

# Step 13 - Configure Firewall

```bash
sudo ufw allow 9000/tcp comment "MinIO API"

sudo ufw allow 9001/tcp comment "MinIO Console"
```

Verify

```bash
sudo ufw status
```

---

# Step 14 - Verify

```bash
ss -tln | grep -E '9000|9001'
```

---

# Step 15 - Open Console

```
http://SERVER_IP:9001
```

Login

```
Username
minioadmin

Password
<Configured Password>
```

---

# Step 16 - Install MinIO Client

In the MinIO Community Edition, user and policy management must be performed exclusively via the mc (MinIO Client) command-line tool

```bash
cd /tmp

wget https://dl.min.io/client/mc/release/linux-amd64/mc

chmod +x mc

sudo mv mc /usr/local/bin/
```

Verify

```bash
mc --version
```

---

# Step 17 - Connect Client

```bash
mc alias set local http://127.0.0.1:9000 minioadmin YOUR_ROOT_PASSWORD
```

Verify

```bash
mc admin info local
```

---

# Step 18 - Create Bucket

```bash
mc mb local/media
```

Ignore the error if it already exists.

Verify

```bash
mc ls local
```

---

# Step 19 - Create Django User

```bash
mc admin user add local django YourStrongPassword
```

Verify

```bash
mc admin user list local
```

---

# Step 20 - Create and Attach a Custom Django Policy (Recommended)

Create a policy file:

```bash
nano django-media-policy.json
```

Paste:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetBucketLocation",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::media"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::media/*"
            ]
        }
    ]
}
```

Create the policy:

```bash
mc admin policy create local django-media django-media-policy.json
```

Attach the policy:

```bash
mc admin policy attach local django-media --user django
```

Verify:

```bash
mc admin user info local django
```

Expected output should show the `django-media` policy attached to the `django` user.

### Homelab Alternative

If you do not need bucket-level restrictions, you can simply attach the built-in `readwrite` policy:

```bash
mc admin policy attach local readwrite --user django
```

This grants read/write access to all buckets and is suitable for small homelab environments.

Useful Administration Commands

| Action        | Command                                           |
| ------------- | ------------------------------------------------- |
| List users    | `mc admin user list local`                        |
| Create user   | `mc admin user add local USER PASSWORD`           |
| Disable user  | `mc admin user disable local USER`                |
| Enable user   | `mc admin user enable local USER`                 |
| Delete user   | `mc admin user remove local USER`                 |
| User details  | `mc admin user info local USER`                   |
| List policies | `mc admin policy list local`                      |
| Show policy   | `mc admin policy info local POLICY`               |
| Create policy | `mc admin policy create local POLICY policy.json` |
| Attach policy | `mc admin policy attach local POLICY --user USER` |
| Detach policy | `mc admin policy detach local POLICY --user USER` |
| Delete policy | `mc admin policy remove local POLICY`             |

---

# Step 21 - Django Environment Variables

```
AWS_ACCESS_KEY_ID=django

AWS_SECRET_ACCESS_KEY=YourStrongPassword

AWS_STORAGE_BUCKET_NAME=media

AWS_S3_ENDPOINT_URL=http://192.168.0.3:9000

AWS_S3_REGION_NAME=us-east-1
```

---

# Step 22 - Install Django Packages

```bash
pip install django-storages boto3
```

---

# Step 23 - Django Configuration (Django 5.1+ / 6.x)

Install the required packages:

```bash
pip install django-storages boto3
```

Add `storages` to your installed apps:

```python
INSTALLED_APPS += [
    "storages",
]
```

Configure the storage backend:

```python
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
```

Configure MinIO:

```python
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")

AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = env("AWS_S3_ENDPOINT_URL")
AWS_S3_REGION_NAME = env("AWS_S3_REGION_NAME", default="us-east-1")

AWS_S3_ADDRESSING_STYLE = "path"
AWS_S3_SIGNATURE_VERSION = "s3v4"

AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_AUTH = False
```

Example `.env`:

```env
AWS_ACCESS_KEY_ID=django
AWS_SECRET_ACCESS_KEY=YourStrongPassword

AWS_STORAGE_BUCKET_NAME=media
AWS_S3_ENDPOINT_URL=http://192.168.0.3:9000
AWS_S3_REGION_NAME=us-east-1
```

---

# Verify Upload

```python
from django.core.files.base import ContentFile

from django.core.files.storage import default_storage

default_storage.save(
    "test.txt",
    ContentFile(b"Hello MinIO")
)
```

The file should appear inside the **media** bucket.

---

# Production Recommendations

- Never use the `minioadmin` account from Django.
- Use HTTPS for MinIO.
- Store credentials in `.env` or Kubernetes Secrets.
- Keep the `media` bucket private.
- Serve downloads using pre-signed URLs.
- Enable bucket versioning.
- Schedule regular backups of the MinIO data directory.
